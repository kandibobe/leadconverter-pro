import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import backend as app  # type: ignore
sys.modules['app'] = app
from app.services import pdf_generator
from app.schemas.lead import LeadOut


def test_generate_pdf_creates_file(tmp_path):
    # Remove default directory created at import to avoid repository pollution
    if os.path.exists(pdf_generator.PDF_STORAGE_PATH):
        shutil.rmtree(pdf_generator.PDF_STORAGE_PATH)

    pdf_generator.PDF_STORAGE_PATH = str(tmp_path)
    os.makedirs(pdf_generator.PDF_STORAGE_PATH, exist_ok=True)

    lead = LeadOut(
        id=1,
        client_email="test@example.com",
        final_price=100.0,
        answers_details={"Question": "Answer"},
    )

    pdf_path = pdf_generator.generate_lead_pdf(lead)

    assert pdf_path.endswith(".pdf")
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 0
