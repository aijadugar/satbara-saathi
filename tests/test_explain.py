from app.models.schema import RulesResult
from app.pipeline.explain import check_hallucination, generate_explanation
from app.providers.fake_providers import FakeLLMProvider


def test_no_hallucination(sample_doc):
    warnings = check_hallucination("This document shows land details.", sample_doc)
    assert warnings == []


def test_generate_with_fake(sample_doc):
    provider = FakeLLMProvider()
    resp = generate_explanation(provider, sample_doc, RulesResult())
    assert resp.summary
    assert resp.disclaimer
