"""Pure-Python validation – no AI, deterministic only."""
import logging
import re

from app.models.schema import Land7x12, key_fields_low_confidence

logger = logging.getLogger(__name__)

SURVEY_PATTERN = re.compile(r"^\d{1,4}(/[A-Z0-9]+)*$")


def validate(doc: Land7x12, threshold: float = 0.85) -> list[str]:
    """Return a list of validation errors (empty = valid)."""
    errors: list[str] = []

    # survey pattern
    sv = doc.survey_or_gat_no.value
    if sv and not SURVEY_PATTERN.match(str(sv)):
        errors.append(f"Survey number '{sv}' does not match expected pattern.")

    # area arithmetic
    c = doc.area.cultivable.value
    p = doc.area.pot_kharab.value
    t = doc.area.total.value
    if c is not None and p is not None and t is not None:
        try:
            if abs((float(c) + float(p)) - float(t)) > 0.02:
                errors.append("Area mismatch: cultivable + pot_kharab != total.")
        except (TypeError, ValueError):
            pass

    # holders not empty
    if not doc.holders:
        errors.append("No holders found on the document.")

    # low-confidence key fields
    low = key_fields_low_confidence(doc, threshold)
    if low:
        errors.append(f"Low-confidence fields need confirmation: {', '.join(low)}")

    return errors
