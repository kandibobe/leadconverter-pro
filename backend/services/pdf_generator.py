import logging
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from backend.schemas.lead import LeadOut

logger = logging.getLogger(__name__)

# Configurable storage path for generated PDFs
PDF_STORAGE_PATH = Path(os.getenv("PDF_STORAGE_PATH", "generated_pdfs"))
PDF_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

PDF_BASE_URL = os.getenv("PDF_BASE_URL")

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def generate_lead_pdf(lead_data: LeadOut) -> str:
    """Generate a PDF estimate for a lead.

    Returns the file path or a download URL if ``PDF_BASE_URL`` is set.
    """
    template = _env.get_template("lead_pdf.html")
    html_content = template.render(lead=lead_data)

    pdf_filename = f"lead_{lead_data.id}_estimate.pdf"
    pdf_filepath = PDF_STORAGE_PATH / pdf_filename

    try:
        HTML(string=html_content).write_pdf(str(pdf_filepath))
        logger.info("PDF generated and saved: %s", pdf_filepath)
    except OSError as exc:
        logger.exception("Failed to write PDF: %s", exc)
        raise

    if PDF_BASE_URL:
        return f"{PDF_BASE_URL.rstrip('/')}/{pdf_filename}"
    return str(pdf_filepath)
