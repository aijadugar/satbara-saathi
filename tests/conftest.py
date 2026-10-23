import pytest
from app.models.schema import *


@pytest.fixture
def sample_doc():
    return Land7x12(
        village=ExtractedField(value="पुणे", confidence=0.98),
        taluka=ExtractedField(value="हवेली", confidence=0.97),
        survey_or_gat_no=ExtractedField(value="37", confidence=0.99),
        khata_no=ExtractedField(value="123", confidence=0.95),
        bhogwatdar_class=ExtractedField(value="1", confidence=0.99),
        holders=[Holder(name=ExtractedField(value="राम जोशी", confidence=0.92))],
        area=Area(
            cultivable=ExtractedField(value=1.0, confidence=0.95),
            pot_kharab=ExtractedField(value=0.25, confidence=0.95),
            total=ExtractedField(value=1.25, confidence=0.95),
        ),
        digitally_signed=ExtractedField(value=True, confidence=0.99),
    )


@pytest.fixture
def flagged_doc(sample_doc):
    sample_doc.other_rights = [
        OtherRight(right_type=ExtractedField(value="Bank Loan", confidence=0.9))
    ]
    sample_doc.tenant_entries = [
        TenantEntry(name=ExtractedField(value="विठ्ठल पवार", confidence=0.88))
    ]
    return sample_doc
