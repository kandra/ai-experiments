from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# Definimos que esperamos un header llamado "x-api-key"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    """
    Verifica que el header 'x-api-key' coincida con nuestra clave secreta.
    """
    if api_key == settings.APP_API_KEY:
        return api_key
    
    # Si no coincide o no existe, lanzamos error 403 (Prohibido)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="🔒 Acceso denegado: API Key inválida o faltante."
    )