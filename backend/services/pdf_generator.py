import os
from weasyprint import HTML
from app.schemas.lead import LeadOut

# Создаем папку для хранения смет, если ее нет
PDF_STORAGE_PATH = "generated_pdfs"
os.makedirs(PDF_STORAGE_PATH, exist_ok=True)

def generate_lead_pdf(lead_data: LeadOut) -> str:
    """
    Генерирует PDF-смету на основе данных лида и сохраняет ее.
    Возвращает путь к файлу.
    """
    # Формируем красивый HTML-шаблон для сметы
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Смета по вашему проекту</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; }}
            .container {{ width: 80%; margin: 0 auto; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .total {{ font-size: 24px; font-weight: bold; text-align: right; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>LeadConverter Pro</h1>
                <p>Предварительная смета на ремонт</p>
            </div>
            <div class="content">
                <p><strong>Клиент:</strong> {lead_data.client_email}</p>
                <h3>Детализация заказа:</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Вопрос</th>
                            <th>Ваш ответ</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for question, answer in lead_data.answers_details.items():
        html_content += f"<tr><td>{question}</td><td>{answer}</td></tr>"

    html_content += f"""
                    </tbody>
                </table>
                <div class="total">
                    Итоговая стоимость: {lead_data.final_price:,.2f} RUB
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Генерируем PDF
    pdf_filename = f"lead_{lead_data.id}_estimate.pdf"
    pdf_filepath = os.path.join(PDF_STORAGE_PATH, pdf_filename)
    
    HTML(string=html_content).write_pdf(pdf_filepath)
    
    print(f"PDF сгенерирован и сохранен: {pdf_filepath}")
    
    # В реальном приложении здесь может быть URL для скачивания
    return pdf_filepath
