"""Deterministic red-flag rules engine. No AI, no eval()."""
import logging
import re
from pathlib import Path

import yaml

from app.models.schema import Flag, Land7x12, RulesResult, Severity

logger = logging.getLogger(__name__)

RULES_PATH = Path(__file__).parent.parent / "rules" / "mh_7_12.yaml"
SEVERITY_ORDER = {Severity.SERIOUS: 0, Severity.CHECK: 1, Severity.INFO: 2}


class RulesEngine:
    def __init__(self, rules_path: Path | None = None):
        path = rules_path or RULES_PATH
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.rules = yaml.safe_load(f).get("rules", [])
        else:
            logger.warning("Rules file not found: %s", path)
            self.rules = []

    def evaluate(self, doc: Land7x12, seller_name: str | None = None) -> RulesResult:
        flags: list[Flag] = []
        for rule in self.rules:
            rid = rule["id"]
            try:
                triggered = self._check(rid, rule, doc, seller_name)
            except Exception:
                logger.exception("Rule %s errored – skipping", rid)
                continue
            if triggered:
                flags.append(Flag(
                    rule_id=rid,
                    severity=Severity(rule["severity"]),
                    title_mr=rule.get("title_mr", ""),
                    title_en=rule.get("title_en", ""),
                    detail_mr=rule.get("explanation_mr", ""),
                    detail_en=rule.get("explanation_en", ""),
                    field_path=rule.get("field_path"),
                    suggestion_mr=rule.get("what_to_do_mr"),
                    suggestion_en=rule.get("what_to_do_en"),
                ))
        flags.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 9))
        return RulesResult(flags=flags, passed=len(flags) == 0)

    # ── individual rule checks (safe, no eval) ─────────────────
    def _check(self, rid: str, rule: dict, doc: Land7x12, seller: str | None) -> bool:
        if rid == "R01":
            keywords = ["bank", "loan", "tagai", "e-karar", "बोजा", "charge", "mortgage", "कर्ज"]
            for r in doc.other_rights:
                text = f"{r.right_type.value or ''} {r.description.value or ''}".lower()
                if any(k in text for k in keywords):
                    return True
            return False

        if rid == "R02":
            return len(doc.holders) > 1

        if rid == "R03":
            return any(h.is_minor_marked.value for h in doc.holders)

        if rid == "R04":
            return doc.bhogwatdar_class.value == "2"

        if rid == "R05":
            return len(doc.tenant_entries) > 0

        if rid == "R06":
            pat = re.compile(
                r"government|govt|महाराष्ट्र|भारत|board|authority|trust|society|company|विद्यापीठ",
                re.IGNORECASE,
            )
            return any(pat.search(h.name.value or "") for h in doc.holders)

        if rid == "R07":
            keywords = ["वारस", "inheritance", "death", "मृत्यू", "legal heir"]
            for m in doc.mutation_entries:
                reason = ((m.reason.value if m.reason else "") or "").lower()
                if any(k in reason for k in keywords):
                    return True
            return False

        if rid == "R08":
            c = doc.area.cultivable.value
            p = doc.area.pot_kharab.value
            t = doc.area.total.value
            if c is not None and p is not None and t is not None:
                try:
                    return abs((float(c) + float(p)) - float(t)) > 0.02
                except (TypeError, ValueError):
                    return False
            return False

        if rid == "R09":
            return not doc.digitally_signed.value and not doc.verification_code_or_qr.value

        if rid == "R10":
            if not seller:
                return False
            seller_lower = seller.lower().strip()
            for h in doc.holders:
                if seller_lower in (h.name.value or "").lower():
                    return False
            return True

        if rid == "R11":
            from app.models.schema import key_fields_low_confidence
            return len(key_fields_low_confidence(doc)) > 0

        return False
