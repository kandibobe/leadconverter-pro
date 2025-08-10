# backend/app/invoicing/facturx_gen.py
from facturx import generate_facturx_from_file, create_facturx_xml
from facturx.facturx import DEFAULT_PROFILES
from pathlib import Path

def build_facturx_pdf(human_pdf_path: str, out_pdf_path: str, data: dict):
    """
    data -> EN16931 semantic model (фактуры).
    Минимум: seller/buyer, VAT, lines, totals. Профиль: EN16931 (ур. COMFORT/BASIC-WL).
    """
    xml = create_facturx_xml(data_dict=data, facturx_level="EN16931")
    generate_facturx_from_file(
        input_pdf_file=Path(human_pdf_path),
        output_pdf_file=Path(out_pdf_path),
        facturx_xml=xml,
        attachments=[],
        check_xsd=True
    )
    return out_pdf_path
