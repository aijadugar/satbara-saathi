"""Explanation pipeline with hallucination post-check."""
import json
import logging
import re

from app.models.schema import ExplanationResponse, Land7x12, Language, RulesResult
from app.providers.base import LLMProvider

logger = logging.getLogger(__name__)


class HallucinationError(Exception):
    pass


def check_hallucination(explanation: str, doc: Land7x12) -> list[str]:
    """Reject output that mentions names/numbers not in the input."""
    warnings: list[str] = []
    input_text = json.dumps(doc.model_dump(), ensure_ascii=False, default=str).lower()
    # look for capitalised multi-word names not in input
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", explanation):
        if m.group(1).lower() not in input_text:
            warnings.append(f"Possible hallucinated name: {m.group(1)}")
    # look for 4+ digit numbers not in input
    for m in re.finditer(r"\b(\d{4,})\b", explanation):
        if m.group(1) not in input_text and not (1900 < int(m.group(1)) < 2100):
            warnings.append(f"Possible hallucinated number: {m.group(1)}")
    return warnings


def generate_explanation(
    provider: LLMProvider,
    doc: Land7x12,
    rules_result: RulesResult,
    language: Language = Language.ENGLISH,
    purpose: str = "general",
    glossary: dict | None = None,
) -> ExplanationResponse:
    payload = {
        "extract_data": doc.model_dump(mode="json"),
        "rules_result": rules_result.model_dump(mode="json"),
        "glossary": glossary or {},
        "purpose": purpose,
    }
    resp = provider.explain(payload, language=language, purpose=purpose)

    # post-check (retry once)
    issues = check_hallucination(resp.summary, doc)
    if issues:
        logger.warning("Hallucination detected (%s), retrying…", issues)
        resp = provider.explain(payload, language=language, purpose=purpose)
        issues = check_hallucination(resp.summary, doc)
        if issues:
            raise HallucinationError(f"Post-check failed twice: {issues}")
    return resp
