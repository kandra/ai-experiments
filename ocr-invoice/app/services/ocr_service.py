import puremagic
from google.cloud import vision
from app.core.config import settings
import os

# Instanciamos el cliente una sola vez al cargar el archivo
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
vision_client = vision.ImageAnnotatorClient()

def detect_mime_type(file_content: bytes) -> str:
    """
    Detecta si es PDF, JPEG, PNG, etc. usando 'números mágicos'.
    """
    try:
        return puremagic.from_string(file_content, mime=True)
    except puremagic.PureError:
        return "application/octet-stream"

def extract_text(file_content: bytes, mime_type: str = None) -> str:
    """
    Orquesta la lectura del texto dependiendo del tipo de archivo.
    """
    if not mime_type:
        mime_type = detect_mime_type(file_content)
        print(f"🕵️‍♀️ Tipo detectado: {mime_type}")

    # Caso A: PDF
    if mime_type == "application/pdf":
        print("📄 Procesando PDF...")
        input_config = vision.InputConfig(content=file_content, mime_type=mime_type)
        feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
        request = vision.AnnotateFileRequest(input_config=input_config, features=[feature])
        
        response = vision_client.batch_annotate_files(requests=[request])
        
        full_text = ""
        for file_res in response.responses:
            for page_res in file_res.responses:
                full_text += page_res.full_text_annotation.text
        return full_text

    # Caso B: Imágenes (JPEG/PNG)
    elif mime_type and mime_type.startswith("image/"):
        print("🖼️ Procesando Imagen...")
        image = vision.Image(content=file_content)
        response = vision_client.text_detection(image=image)
        if response.text_annotations:
            return response.text_annotations[0].description
        return ""
    
    else:
        raise ValueError(f"⚠️ Tipo de archivo no soportado: {mime_type}")