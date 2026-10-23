"""Pydantic v2 models for Maharashtra 7/12 extract processing."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ── Enums ────────────────────────────────────────────────────────
class Language(str, Enum):
    ENGLISH = "en"
    MARATHI = "mr"
    HINDI = "hi"


class Severity(str, Enum):
    INFO = "info"
    CHECK = "check"
    SERIOUS = "serious"


class AreaUnit(str, Enum):
    HECTARE_ARE = "hectare-are"
    SQ_M = "sq_m"
    GUNTHA = "guntha"


class OccupancyClass(str, Enum):
    CLASS_1 = "1"
    CLASS_2 = "2"


# ── Generic extracted-field wrapper ─────────────────────────────
class ExtractedField(BaseModel, Generic[T]):
    """Every OCR-extracted value carries confidence + source text."""
    value: T | None = None
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = 0.0
    source_text: str | None = None
    bbox: list[float] | None = Field(default=None, min_length=4, max_length=4)

    @property
    def is_empty(self) -> bool:
        return self.value is None

    def is_low_confidence(self, threshold: float = 0.85) -> bool:
        return self.confidence < threshold


# ── OCR models ───────────────────────────────────────────────────
class OCRWord(BaseModel):
    text: str
    conf: Annotated[float, Field(ge=0.0, le=1.0)] = 1.0
    bbox: list[float] | None = Field(default=None, min_length=4, max_length=4)


class OCRPage(BaseModel):
    page_number: int
    words: list[OCRWord] = Field(default_factory=list)
    full_text: str = ""
    avg_confidence: Annotated[float, Field(ge=0.0, le=1.0)] = 0.0


class OCRResult(BaseModel):
    pages: list[OCRPage] = Field(default_factory=list)
    full_text: str = ""
    model_config = ConfigDict(extra="allow")

    @property
    def total_words(self) -> int:
        return sum(len(p.words) for p in self.pages)

    @property
    def avg_confidence(self) -> float:
        if not self.pages:
            return 0.0
        return sum(p.avg_confidence for p in self.pages) / len(self.pages)


# ── 7/12 sub-models ─────────────────────────────────────────────
class Holder(BaseModel):
    name: ExtractedField[str] = Field(default_factory=ExtractedField)
    share_text: ExtractedField[str] = Field(default_factory=ExtractedField)
    is_minor_marked: ExtractedField[bool] = Field(default_factory=ExtractedField)
    guardian_name: ExtractedField[str] = Field(default_factory=ExtractedField)
    holder_number: int | None = None


class Area(BaseModel):
    cultivable: ExtractedField[float] = Field(default_factory=ExtractedField)
    pot_kharab: ExtractedField[float] = Field(default_factory=ExtractedField)
    total: ExtractedField[float] = Field(default_factory=ExtractedField)
    unit: ExtractedField[AreaUnit] = Field(default_factory=ExtractedField)


class TenantEntry(BaseModel):
    name: ExtractedField[str] = Field(default_factory=ExtractedField)
    rent_text: ExtractedField[str] = Field(default_factory=ExtractedField)
    survey_no: ExtractedField[str] | None = None
    entry_number: int | None = None


class OtherRight(BaseModel):
    right_type: ExtractedField[str] = Field(default_factory=ExtractedField)
    description: ExtractedField[str] = Field(default_factory=ExtractedField)
    holder_or_charge: ExtractedField[str] = Field(default_factory=ExtractedField)
    amount: ExtractedField[str] | None = None
    document_ref: ExtractedField[str] | None = None


class MutationEntry(BaseModel):
    ferfar_number: ExtractedField[str] = Field(default_factory=ExtractedField)
    date: ExtractedField[str] | None = None
    from_person: ExtractedField[str] | None = None
    to_person: ExtractedField[str] | None = None
    reason: ExtractedField[str] | None = None


class CropEntry(BaseModel):
    crop_name: ExtractedField[str] = Field(default_factory=ExtractedField)
    season: ExtractedField[str] = Field(default_factory=ExtractedField)
    area_under_crop: ExtractedField[float] = Field(default_factory=ExtractedField)


# ── Main 7/12 model ─────────────────────────────────────────────
class Land7x12(BaseModel):
    village: ExtractedField[str] = Field(default_factory=ExtractedField)
    taluka: ExtractedField[str] = Field(default_factory=ExtractedField)
    district: ExtractedField[str] = Field(default_factory=ExtractedField)

    survey_or_gat_no: ExtractedField[str] = Field(default_factory=ExtractedField)
    sub_division_no: ExtractedField[str] | None = None
    khata_no: ExtractedField[str] = Field(default_factory=ExtractedField)

    bhogwatdar_class: ExtractedField[OccupancyClass] = Field(default_factory=ExtractedField)
    holders: list[Holder] = Field(default_factory=list)

    area: Area = Field(default_factory=Area)
    assessment: ExtractedField[str] = Field(default_factory=ExtractedField)

    other_rights: list[OtherRight] = Field(default_factory=list)
    tenant_entries: list[TenantEntry] = Field(default_factory=list)
    mutation_numbers: list[str] = Field(default_factory=list)
    mutation_entries: list[MutationEntry] = Field(default_factory=list)
    crop_entries: list[CropEntry] = Field(default_factory=list)

    digitally_signed: ExtractedField[bool] = Field(default_factory=ExtractedField)
    verification_code_or_qr: ExtractedField[str] = Field(default_factory=ExtractedField)
    extract_date: ExtractedField[datetime] = Field(default_factory=ExtractedField)
    extract_number: ExtractedField[str] | None = None
    revenue_year: ExtractedField[str] | None = None

    model_config = ConfigDict(extra="allow")


# ── Rules / Flags ────────────────────────────────────────────────
class Flag(BaseModel):
    rule_id: str
    severity: Severity
    title_mr: str
    title_hi: str = ""
    title_en: str
    detail_mr: str
    detail_hi: str = ""
    detail_en: str
    evidence: list[str] = Field(default_factory=list)
    field_path: str | None = None
    suggestion_mr: str | None = None
    suggestion_hi: str | None = None
    suggestion_en: str | None = None


class RulesResult(BaseModel):
    flags: list[Flag] = Field(default_factory=list)
    passed: bool = True


# ── Explanation ──────────────────────────────────────────────────
class ExplanationRequest(BaseModel):
    extract_data: Land7x12
    rules_result: RulesResult
    language: Language = Language.ENGLISH
    user_confirmations: dict[str, str] | None = None


class ExplanationResponse(BaseModel):
    summary: str
    field_explanations: dict[str, str] = Field(default_factory=dict)
    flag_explanations: dict[str, str] = Field(default_factory=dict)
    disclaimer: str
    model_used: str | None = None
    tokens_used: int | None = None


# ── Speech ───────────────────────────────────────────────────────
class SpeechRequest(BaseModel):
    text: str
    language: Language = Language.MARATHI
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class SpeechResponse(BaseModel):
    audio: bytes
    format: str = "mp3"
    duration_seconds: float | None = None


# ── Processing status ────────────────────────────────────────────
class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFIRMATION_REQUIRED = "confirmation_required"


class ProcessingResult(BaseModel):
    job_id: str
    status: ProcessingStatus
    extract: Land7x12 | None = None
    rules_result: RulesResult | None = None
    explanation: ExplanationResponse | None = None
    confirmation_fields: list[dict[str, Any]] = Field(default_factory=list)
    disclaimer: str = (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Please consult a qualified advocate."
    )
    errors: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    version: str
    providers: dict[str, str] = Field(default_factory=dict)
    privacy_mode: bool = True


# ── Helper ───────────────────────────────────────────────────────
def key_fields_low_confidence(doc: Land7x12, threshold: float = 0.85) -> list[str]:
    """Return field paths whose OCR confidence is below *threshold*."""
    low: list[str] = []
    if doc.survey_or_gat_no.is_low_confidence(threshold):
        low.append("survey_or_gat_no")
    if doc.khata_no.is_low_confidence(threshold):
        low.append("khata_no")
    for i, h in enumerate(doc.holders):
        if h.name.is_low_confidence(threshold):
            low.append(f"holders[{i}].name")
    if doc.area.total.is_low_confidence(threshold):
        low.append("area.total")
    if doc.bhogwatdar_class.is_low_confidence(threshold):
        low.append("bhogwatdar_class")
    for i, r in enumerate(doc.other_rights):
        if r.right_type.is_low_confidence(threshold):
            low.append(f"other_rights[{i}].right_type")
    return low
