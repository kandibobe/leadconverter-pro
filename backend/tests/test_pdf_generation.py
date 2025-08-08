import os

from app.schemas.lead import LeadOut
from app.services import pdf_generator


def test_generate_lead_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_generator, "PDF_STORAGE_PATH", str(tmp_path))
    os.makedirs(tmp_path, exist_ok=True)
    lead = LeadOut(
        id=1,
        client_email="user@example.com",
        final_price=100.0,
        answers_details={"Q": "A"},
        tenant_id="t",
    )
    path = pdf_generator.generate_lead_pdf(lead)
    assert os.path.exists(path)

