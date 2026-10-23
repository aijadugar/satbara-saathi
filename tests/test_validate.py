from app.models.schema import ExtractedField
from app.pipeline.validate import validate


def test_valid_doc(sample_doc):
    assert validate(sample_doc) == []


def test_area_mismatch(sample_doc):
    sample_doc.area.total = ExtractedField(value=99.0, confidence=0.95)
    errs = validate(sample_doc)
    assert any("Area mismatch" in e for e in errs)


def test_empty_holders(sample_doc):
    sample_doc.holders = []
    assert any("No holders" in e for e in validate(sample_doc))
