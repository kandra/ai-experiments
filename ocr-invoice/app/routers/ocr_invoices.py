from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services import ocr_service, ai_service, db_service
from app.core.security import validate_api_key
import json

# Creamos el router (como una "mini app")
router = APIRouter()


# Esto protege TODAS las rutas que estén debajo de este router, 
# o puedes ponerlo solo en el @router.post si prefieres.
@router.post("/ocr-invoice", dependencies=[Depends(validate_api_key)])
async def process_invoice(file: UploadFile = File(...)):
    print(f"📥 Recibido: {file.filename}")
    
    try:
        # 1. Leer bytes del archivo
        file_content = await file.read()
        
        # 2. Servicio de OCR: Bytes -> Texto
        raw_text = ocr_service.extract_text(file_content)
        
        # 3. Servicio de IA: Texto -> JSON
        json_str = ai_service.parse_invoice_text(raw_text)
        parsed_data = json.loads(json_str)
        
        # 4. Servicio de DB: JSON -> SQL
        invoice_id = db_service.save_invoice_data(parsed_data, file_url=file.filename)
        
        return {
            "status": "success",
            "invoice_id": invoice_id,
            "data": parsed_data
        }

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
        raise HTTPException(status_code=500, detail=str(e))