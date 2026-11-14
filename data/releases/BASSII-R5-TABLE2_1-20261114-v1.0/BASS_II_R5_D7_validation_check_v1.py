#!/usr/bin/env python3
"""Standalone integrity and semantic release checks; NOT NASA-EVP scientific verification."""
from pathlib import Path
from decimal import Decimal
from collections import Counter
import csv, hashlib, json, sys

ROOT=Path(__file__).resolve().parent
PREFIX="BASS_II_R5_D7_"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))

def check():
    m=json.loads((ROOT/(PREFIX+'manifest_v1.json')).read_text(encoding='utf-8'))
    for name,item in m['files'].items():
        path=ROOT/name
        assert path.is_file(),f'missing: {name}'
        assert sha(path)==item['sha256'],f'SHA mismatch: {name}'
        assert path.stat().st_size==item['byte_size'],f'byte-size mismatch: {name}'
    print('PASS: payload SHA-256 and byte sizes match manifest')
    raw=rows(ROOT/(PREFIX+'raw_2rows_v1.csv'))
    c=rows(ROOT/(PREFIX+'curated_6cells_v1.csv'))
    q=rows(ROOT/(PREFIX+'QC_6cells_v1.csv'))
    assert len(raw)==2 and len(c)==6 and len(q)==6
    assert set(r['o2_percent_raw'] for r in raw)=={'21','16'}
    assert len({r['evidence_cell_id'] for r in c})==6
    assert {r['evidence_cell_id'] for r in c}=={r['evidence_cell_id'] for r in q}
    print('PASS: 2 original rows, 6 unique evidence cells, 6 QC matches')
    expect={('21','EXPERIMENTAL'):('10±5','10','5'),('21','COMPUTATIONAL_MODEL'):('15','15',''),('21','ANALYTICAL_MODEL'):('7.5','7.5',''),('16','EXPERIMENTAL'):('30±5','30','5'),('16','COMPUTATIONAL_MODEL'):('35','35',''),('16','ANALYTICAL_MODEL'):('10','10','')}
    for r in c:
        k=(r['oxygen_percent_raw'],r['method_origin'])
        assert k in expect
        assert (r['critical_velocity_raw'],r['critical_velocity_center_mm_per_s'],r['experimental_uncertainty_mm_per_s'])==expect[k]
        assert Decimal(r['oxygen_fraction_normalized'])==Decimal(r['oxygen_percent_raw'])/Decimal(100)
        assert r['original_test_id']==''
        assert r['critical_velocity_raw_unit']=='mm/s'
        assert r['source_anchor'].startswith('NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1|')
        assert r['transcription_review_status']=='VERIFIED'
        assert r['scientific_fitness_status']=='CONDITIONAL_GO_ONLY'
        if r['method_origin']!='EXPERIMENTAL':
            assert r['uncertainty_status']=='NOT_REPORTED'
    print('PASS: raw strings, method origins, uncertainty distinctions and exact Decimal oxygen conversions')
    assert all('UNQUALIFIED_CAUSAL_OXYGEN_EFFECT' in z['blocked_uses'] for z in q)
    assert all(z['original_test_linkage']=='UNRESOLVED' for z in q)
    print('PASS: source anchors and scientific block flags preserved')
    cases=json.loads((ROOT/(PREFIX+'proposed_claims_v1.json')).read_text(encoding='utf-8'))['cases']
    assert len(cases)==10
    assert Counter(x['category'] for x in cases)=={'positive':4,'negative_value':1,'negative_unit':1,'overclaim':2,'out_of_scope':2}
    assert all(x['execution_status']=='PROPOSED_NOT_RUN' for x in cases)
    print('PASS: 10 predefined proposed claims; none mislabeled as executed')
    print('PASS: bounded NASA-DAP D7 release integrity checks complete')

if __name__=='__main__':
    try:check()
    except Exception as e:
        print(f'FAIL: {type(e).__name__}: {e}',file=sys.stderr)
        sys.exit(1)
