
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from src.handlers import router as handlers_router
from src import database

# Cargamos variables del archivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se encontró TELEGRAM_BOT_TOKEN en el archivo .env")

bot = Bot(token=TOKEN)
# Administra los mensajes que recibe el bot
dp = Dispatcher()

dp.include_router(handlers_router)


async def main():
    await database.conectar(os.getenv("DATABASE_URL"))
    try:
        print("Iniciando bot...")
        # Mantenemos el programa consultando a Telegram para recibir actualizaciones
        await dp.start_polling(bot)
    finally:
        await database.desconectar()


if __name__ == "__main__":
    asyncio.run(main())