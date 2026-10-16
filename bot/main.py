
import asyncio

from aiogram import Bot, Dispatcher

from src import database
from src.config import DATABASE_URL, TOKEN
from src.handlers import router as handlers_router

bot = Bot(token=TOKEN)
# Administra los mensajes que recibe el bot
dp = Dispatcher()

dp.include_router(handlers_router)


async def main():
    await database.conectar(DATABASE_URL)
    try:
        print("Iniciando bot...")
        # Mantenemos el programa consultando a Telegram para recibir actualizaciones
        await dp.start_polling(bot)
    finally:
        await database.desconectar()


if __name__ == "__main__":
    asyncio.run(main())
