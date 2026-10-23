from app.models.schema import *


def test_extracted_field_defaults():
    f = ExtractedField()
    assert f.is_empty
    assert f.confidence == 0.0


def test_key_fields_low_confidence(sample_doc):
    sample_doc.survey_or_gat_no = ExtractedField(value="37", confidence=0.5)
    low = key_fields_low_confidence(sample_doc)
    assert "survey_or_gat_no" in low


def test_land712_serialisation(sample_doc):
    d = sample_doc.model_dump()
    assert d["village"]["value"] == "पुणे"
