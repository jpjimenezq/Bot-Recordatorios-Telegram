import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

# Cargamos variables del archivo .env (en Docker no existe; las variables vienen de docker-compose)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Zona horaria del usuario: las fechas se guardan con esta zona y se muestran en ella
ZONA = ZoneInfo(os.getenv("ZONA", "America/Bogota"))

if not TOKEN:
    raise ValueError("No se encontró TELEGRAM_BOT_TOKEN en el archivo .env")

if not DATABASE_URL:
    raise ValueError("No se encontró DATABASE_URL en el archivo .env")
