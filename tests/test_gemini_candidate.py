"""Offline tests: never spend Gemini quota or require an API key."""

import json
from types import SimpleNamespace

import pytest

from src.gemini_candidate import (
    CandidateRejected, EvidenceSnippet, GeminiCallError, generate_candidate,
)


def sample(study="BASS-II", evidence_id="BASS_EXPERIMENT"):
    return EvidenceSnippet(
        study=study,
        evidence_id=evidence_id,
        source_locator="NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1",
        source_text="Experimental critical velocity reported with uncertainty.",
        restrictions="No causal inference; as-run mapping unresolved.",
    )


class FakeClient:
    def __init__(self, payload=None, error=None):
        self.payload = payload or {
            "interpretation": "The report presents a bounded comparison, not a general safety rule.",
            "cited_evidence_ids": ["BASS_EXPERIMENT"],
            "limitations": ["Unique run mapping is unresolved."],
        }
        self.error = error
        self.calls = []
        self.models = self

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return SimpleNamespace(text=json.dumps(self.payload))


def test_valid_draft_is_never_scientifically_supported():
    client = FakeClient()
    result = generate_candidate("Explain the source restriction", [sample()], client=client)
    assert result["status"] == "CANDIDATE_NOT_VERIFIED"
    assert result["validation"] == "CITATION_IDS_AND_FORMAT_ONLY"
    assert result["source_locators"]["BASS_EXPERIMENT"].endswith("Table_2.1")
    assert client.calls[0]["config"]["response_mime_type"] == "application/json"
    assert '"evidence_id": "BASS_EXPERIMENT"' in client.calls[0]["contents"]


def test_unknown_citation_is_rejected():
    client = FakeClient(payload={
        "interpretation": "A draft.",
        "cited_evidence_ids": ["INVENTED"],
        "limitations": ["Not independently verified."],
    })
    with pytest.raises(CandidateRejected, match="evidence citations"):
        generate_candidate("Explain", [sample()], client=client)


def test_numeric_prose_is_rejected():
    client = FakeClient(payload={
        "interpretation": "The threshold is 999 mm/s.",
        "cited_evidence_ids": ["BASS_EXPERIMENT"],
        "limitations": ["No qualification."],
    })
    with pytest.raises(CandidateRejected, match="Numerical"):
        generate_candidate("Explain", [sample()], client=client)


def test_missing_limitations_are_rejected():
    client = FakeClient(payload={
        "interpretation": "A draft.",
        "cited_evidence_ids": ["BASS_EXPERIMENT"],
        "limitations": [],
    })
    with pytest.raises(CandidateRejected, match="limitations"):
        generate_candidate("Explain", [sample()], client=client)


def test_cross_study_is_blocked_before_call():
    client = FakeClient()
    with pytest.raises(CandidateRejected, match="Cross-study"):
        generate_candidate("Compare", [sample(), sample("FLEX", "FLEX-001")], client=client)
    assert client.calls == []


def test_api_exception_does_not_leak_secret():
    client = FakeClient(error=RuntimeError("SECRET_API_KEY_123"))
    with pytest.raises(GeminiCallError) as raised:
        generate_candidate("Explain", [sample()], client=client)
    assert "SECRET_API_KEY_123" not in str(raised.value)


def test_invalid_json_is_rejected():
    client = FakeClient()
    client.generate_content = lambda **kwargs: SimpleNamespace(text="not-json")
    with pytest.raises(CandidateRejected, match="valid JSON"):
        generate_candidate("Explain", [sample()], client=client)


def test_unbounded_source_payload_is_blocked():
    snippet = sample()
    oversized = EvidenceSnippet(snippet.study, snippet.evidence_id, snippet.source_locator,
                                "A" * 1201, snippet.restrictions)
    with pytest.raises(CandidateRejected, match="source text"):
        generate_candidate("Explain", [oversized], client=FakeClient())


def test_real_bassii_evidence_id_separator_is_allowed():
    evidence_id = "BASSII_T2_1_O2_21pct|EXPERIMENTAL"
    client = FakeClient(payload={
        "interpretation": "This is a bounded report summary, not a universal rule.",
        "cited_evidence_ids": [evidence_id],
        "limitations": ["Unique as-run test mapping is unresolved."],
    })
    result = generate_candidate(
        "Summarize the published report cell",
        [sample(evidence_id=evidence_id)],
        client=client,
    )
    assert result["cited_evidence_ids"] == [evidence_id]
    assert result["status"] == "CANDIDATE_NOT_VERIFIED"
