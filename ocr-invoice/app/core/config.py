import os
from dotenv import load_dotenv

# Cargar el archivo .env una sola vez al inicio
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI/OCR Invoice Parser"
    VERSION: str = "1.0.0"
    
    # Variables obligatorias (si fallan, la app no arranca)
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    APP_API_KEY: str = os.getenv("APP_API_KEY")

    def validate(self):
        """Verifica que las variables críticas existan."""
        if not self.DATABASE_URL:
            raise ValueError("❌ Error Crítico: Falta DATABASE_URL en el archivo .env")
        if not self.GOOGLE_API_KEY:
            raise ValueError("❌ Error Crítico: Falta GOOGLE_API_KEY en el archivo .env")
        if not os.path.exists(self.GOOGLE_APPLICATION_CREDENTIALS):
            raise ValueError(f"❌ No encuentro el archivo de credenciales en: {self.GOOGLE_APPLICATION_CREDENTIALS}")
        if not self.APP_API_KEY:
            raise ValueError("❌ Falta APP_API_KEY en el archivo .env")

# Instanciamos la clase para importarla desde otros lados
settings = Settings()
settings.validate()