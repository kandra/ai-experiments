import psycopg2
from app.core.config import settings

def get_db_connection():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        # En producción, aquí podrías loguear el error a un sistema de monitoreo
        raise e