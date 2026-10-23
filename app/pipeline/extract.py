"""Structured extraction: OCRResult → Land7x12."""
import logging

from app.models.schema import (
    Area,
    ExtractedField,
    Holder,
    Land7x12,
    OCRResult,
    OtherRight,
    TenantEntry,
)

logger = logging.getLogger(__name__)

DEV_TO_ASCII = str.maketrans("०१२३४५६७८९", "0123456789")


def devanagari_to_ascii(text: str) -> str:
    return text.translate(DEV_TO_ASCII) if text else text


def extract_from_structured(data: dict, ocr: OCRResult | None = None) -> Land7x12:
    """Build Land7x12 from a structured-extraction dict."""
    def ef(key: str, default=None) -> ExtractedField:
        raw = data.get(key, {})
        if isinstance(raw, dict):
            return ExtractedField(
                value=raw.get("value", default),
                confidence=raw.get("confidence", 0.9),
                source_text=raw.get("source_text"),
                bbox=raw.get("bbox"),
            )
        return ExtractedField(value=raw if raw is not None else default, confidence=0.9)

    holders = []
    for i, h in enumerate(data.get("holders", [])):
        holders.append(Holder(
            name=ef("name") if not isinstance(h, dict) else ExtractedField(
                value=h.get("name", {}).get("value"),
                confidence=h.get("name", {}).get("confidence", 0.85),
                source_text=h.get("name", {}).get("source_text"),
            ),
            share_text=ExtractedField(
                value=h.get("share_text", {}).get("value") if isinstance(h, dict) else None,
                confidence=0.8,
            ),
            is_minor_marked=ExtractedField(
                value=h.get("is_minor_marked", {}).get("value", False) if isinstance(h, dict) else False,
                confidence=0.95,
            ),
            guardian_name=ExtractedField(
                value=h.get("guardian_name", {}).get("value") if isinstance(h, dict) else None,
                confidence=0.8,
            ),
            holder_number=i + 1,
        ))

    area_raw = data.get("area", {})
    area = Area(
        cultivable=ExtractedField(value=area_raw.get("cultivable", {}).get("value") if isinstance(area_raw.get("cultivable"), dict) else area_raw.get("cultivable"), confidence=0.9),
        pot_kharab=ExtractedField(value=area_raw.get("pot_kharab", {}).get("value") if isinstance(area_raw.get("pot_kharab"), dict) else area_raw.get("pot_kharab"), confidence=0.9),
        total=ExtractedField(value=area_raw.get("total", {}).get("value") if isinstance(area_raw.get("total"), dict) else area_raw.get("total"), confidence=0.9),
        unit=ExtractedField(value=area_raw.get("unit", {}).get("value") if isinstance(area_raw.get("unit"), dict) else area_raw.get("unit"), confidence=0.95),
    )

    other_rights = []
    for r in data.get("other_rights", []):
        if isinstance(r, dict):
            other_rights.append(OtherRight(
                right_type=ExtractedField(value=r.get("right_type", {}).get("value", ""), confidence=0.85),
                description=ExtractedField(value=r.get("description", {}).get("value", ""), confidence=0.85),
                holder_or_charge=ExtractedField(value=r.get("holder_or_charge", {}).get("value", ""), confidence=0.85),
            ))

    tenants = []
    for t in data.get("tenant_entries", []):
        if isinstance(t, dict):
            tenants.append(TenantEntry(
                name=ExtractedField(value=t.get("name", {}).get("value", ""), confidence=0.85),
                rent_text=ExtractedField(value=t.get("rent_text", {}).get("value", ""), confidence=0.85),
            ))

    return Land7x12(
        village=ef("village"),
        taluka=ef("taluka"),
        district=ef("district"),
        survey_or_gat_no=ef("survey_or_gat_no"),
        khata_no=ef("khata_no"),
        bhogwatdar_class=ef("bhogwatdar_class"),
        holders=holders,
        area=area,
        assessment=ef("assessment"),
        other_rights=other_rights,
        tenant_entries=tenants,
        mutation_numbers=data.get("mutation_numbers", []),
        digitally_signed=ef("digitally_signed"),
        verification_code_or_qr=ef("verification_code_or_qr"),
    )
