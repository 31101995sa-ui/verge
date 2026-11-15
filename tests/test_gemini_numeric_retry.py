"""Offline fail-closed Gemini retry tests, no API quota needed."""

import json
from types import SimpleNamespace

import pytest

from src.gemini_candidate import CandidateRejected, EvidenceSnippet, generate_candidate


class SequentialClient:
    def __init__(self, payloads):
        self.payloads = payloads
        self.calls = []
        self.models = self

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(text=json.dumps(self.payloads[len(self.calls) - 1]))


def source():
    return EvidenceSnippet(
        study="FLEX",
        evidence_id="FLEX-002",
        source_locator="NASA/TP-2015-216046|Table_IX|FLEX-002",
        source_text="Reported data for a selected source row.",
        restrictions="No causal inference or universal thresholds.",
    )


def draft(text, cited=None):
    return {
        "interpretation": text,
        "cited_evidence_ids": cited or ["FLEX-002"],
        "limitations": ["No causal inference is justified."],
    }


def test_numeric_prose_gets_one_reprompt_then_accepted_if_clean():
    fake = SequentialClient([draft("Test FLEX-002 describes a droplet."),
                             draft("The report describes an individual droplet observation.")])
    result = generate_candidate("Объясни наблюдения без чисел", [source()], client=fake)
    assert len(fake.calls) == 2
    assert "NO digits" in fake.calls[1]["config"]["system_instruction"]
    assert result["interpretation"].startswith("The report")
    assert result["status"] == "CANDIDATE_NOT_VERIFIED"


def test_second_numeric_answer_stays_rejected_no_third_call():
    fake = SequentialClient([draft("Test FLEX-002."), draft("Test FLEX-002 again.")])
    with pytest.raises(CandidateRejected, match="Numerical LLM prose"):
        generate_candidate("Describe", [source()], client=fake)
    assert len(fake.calls) == 2


def test_unknown_citation_does_not_trigger_retry():
    fake = SequentialClient([draft("Bounded observation.", ["FAKE_ID"])])
    with pytest.raises(CandidateRejected, match="evidence citations"):
        generate_candidate("Describe", [source()], client=fake)
    assert len(fake.calls) == 1


def test_valid_answer_does_not_trigger_retry():
    fake = SequentialClient([draft("Bounded observation.")])
    result = generate_candidate("Describe", [source()], client=fake)
    assert result["validation"] == "CITATION_IDS_AND_FORMAT_ONLY"
    assert len(fake.calls) == 1
