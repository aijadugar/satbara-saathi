from app.models.schema import ExtractedField, Holder
from app.pipeline.rules import RulesEngine

engine = RulesEngine()


def test_r01_bank_loan(flagged_doc):
    r = engine.evaluate(flagged_doc)
    assert any(f.rule_id == "R01" for f in r.flags)


def test_r02_multiple_holders(sample_doc):
    sample_doc.holders.append(Holder(name=ExtractedField(value="सीता जोशी", confidence=0.9)))
    r = engine.evaluate(sample_doc)
    assert any(f.rule_id == "R02" for f in r.flags)


def test_r05_tenant(flagged_doc):
    r = engine.evaluate(flagged_doc)
    assert any(f.rule_id == "R05" for f in r.flags)


def test_clean_doc(sample_doc):
    r = engine.evaluate(sample_doc)
    assert r.passed


def test_severity_sort(flagged_doc):
    r = engine.evaluate(flagged_doc)
    severities = [f.severity.value for f in r.flags]
    order = {"serious": 0, "check": 1, "info": 2}
    assert severities == sorted(severities, key=lambda s: order[s])
