import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from app.schemas.lead import LeadOut

# Создаем папку для хранения смет, если ее нет
PDF_STORAGE_PATH = "generated_pdfs"
os.makedirs(PDF_STORAGE_PATH, exist_ok=True)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)

def generate_lead_pdf(lead_data: LeadOut) -> str:
    """
    Генерирует PDF-смету на основе данных лида и сохраняет ее.
    Возвращает путь к файлу.
    """
    template = _env.get_template("lead_pdf.html")
    html_content = template.render(lead=lead_data)

    # Генерируем PDF
    pdf_filename = f"lead_{lead_data.id}_estimate.pdf"
    pdf_filepath = os.path.join(PDF_STORAGE_PATH, pdf_filename)

    HTML(string=html_content).write_pdf(pdf_filepath)

    print(f"PDF сгенерирован и сохранен: {pdf_filepath}")

    # В реальном приложении здесь может быть URL для скачивания
    return pdf_filepath
