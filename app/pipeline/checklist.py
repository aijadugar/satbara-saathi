"""Build a 'Next steps' checklist from triggered flags and purpose."""
from app.models.schema import Language, RulesResult

UNIVERSAL = [
    {"title_en": "Verify on Mahabhulekh portal", "title_mr": "महाभूलेख पोर्टलवर सत्यापन करा",
     "url": "https://mahabhulekh.maharashtra.gov.in"},
    {"title_en": "Check for pending mutations at talathi office", "title_mr": "तलाठी कार्यालयात प्रलंबित फेरफार तपासा"},
]

FLAG_STEPS = {
    "R01": {"title_en": "Confirm loan status with the bank", "title_mr": "बँकेशी कर्ज स्थिती तपासा"},
    "R02": {"title_en": "Get consent from all co-owners", "title_mr": "सर्व सहमालकांची संमती मिळवा"},
    "R03": {"title_en": "Verify guardian authority / court permission", "title_mr": "पालक अधिकार / न्यायालय परवानगी तपासा"},
    "R04": {"title_en": "Check transfer permission with revenue office", "title_mr": "महसूल कार्यालयात हस्तांतरण परवानगी तपासा"},
    "R05": {"title_en": "Check tenant rights and get consent", "title_mr": "कुळ अधिकार तपासा आणि संमती मिळवा"},
    "R06": {"title_en": "Verify institutional transfer procedure", "title_mr": "संस्था हस्तांतरण प्रक्रिया तपासा"},
    "R07": {"title_en": "Verify chain of title / heir certificates", "title_mr": "मालकी साखळी / वारसा प्रमाणपत्र तपासा"},
    "R08": {"title_en": "Re-verify area figures with original document", "title_mr": "मूळ दस्तऐवजासह क्षेत्रफळ पुन्हा तपासा"},
    "R09": {"title_en": "Verify extract on official portal", "title_mr": "अधिकृत पोर्टलवर उतारा सत्यापित करा"},
    "R10": {"title_en": "Confirm seller identity matches holders", "title_mr": "विक्रेता ओळख धारकांशी जुळते याची खात्री करा"},
}

BUYING_EXTRA = [
    {"title_en": "Get a title search report from a lawyer", "title_mr": "वकिलाकडून मालकी शोध अहवाल मिळवा"},
]

LOAN_EXTRA = [
    {"title_en": "Get property valuation from approved valuer", "title_mr": "मान्यताप्राप्त मूल्यमापकाकडून मालमत्ता मूल्यांकन मिळवा"},
]


def generate_checklist(
    rules_result: RulesResult,
    purpose: str = "general",
    language: Language = Language.ENGLISH,
) -> list[dict]:
    triggered = {f.rule_id for f in rules_result.flags}
    items: list[dict] = []
    step = 1

    for u in UNIVERSAL:
        key = "title_mr" if language == Language.MARATHI else "title_en"
        items.append({"step": step, "title": u.get(key, u["title_en"]), "url": u.get("url")})
        step += 1

    for rid, s in FLAG_STEPS.items():
        if rid in triggered:
            key = "title_mr" if language == Language.MARATHI else "title_en"
            items.append({"step": step, "title": s.get(key, s["title_en"])})
            step += 1

    extras = BUYING_EXTRA if purpose == "buying" else LOAN_EXTRA if purpose == "loan" else []
    for e in extras:
        key = "title_mr" if language == Language.MARATHI else "title_en"
        items.append({"step": step, "title": e.get(key, e["title_en"])})
        step += 1

    return items
