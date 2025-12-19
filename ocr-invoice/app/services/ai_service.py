from google import genai
from app.core.config import settings

# Usamos la configuración centralizada
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

def parse_invoice_text(ocr_text: str) -> str:
    """
    Envía el texto crudo a Gemini y retorna el JSON limpio.
    """
    system_prompt = """
    You are an expert data extraction assistant specialized in financial documents.
    Your Goal: Extract structured data from the provided invoice text and return it strictly as valid JSON.
    
    Extraction Rules:
    1. Dates: Convert all dates to YYYY-MM-DD format.
    2. Numbers: Return numeric values as numbers (e.g., 16.00), not strings.
    3. Currency: Detect the currency code (e.g., PEN, USD).
    4. Categories: Infer a broad category in Spanish (e.g., 'Limpieza', 'Oficina', 'Abarrotes').
    5. Vendor Info: Extract Name, RUC, Phone, and Email if available.
    
    JSON Output Schema:
    {
      "invoice_details": {
        "vendor_name": "string",
        "vendor_ruc": "string",
        "vendor_phone": "string",
        "vendor_email": "string",
        "invoice_number": "string",
        "date": "YYYY-MM-DD",
        "currency": "string",
        "total_amount": number
      },
      "line_items": [
        {
          "description": "string",
          "quantity": number,
          "unit_price": number,
          "total_price": number,
          "category": "string"
        }
      ]
    }
    """

    full_prompt = system_prompt + "\n\nInput Text:\n" + ocr_text

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt
    )

    # Limpieza básica del markdown
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return clean_json