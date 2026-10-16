import inspect

from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

router = Router()

recordatorios = {}
siguiente_id = 1


@router.message(CommandStart())
async def start_handler(message: Message):
    msg = inspect.cleandoc("""
    ¡Hola! Soy tu bot de recordatorios.
    Puedo ayudarte a guardar y recibir recordatorios.
    """)
    await message.answer(msg)


@router.message(Command("help"))
async def help_handler(message: Message):
    msg = inspect.cleandoc("""
    Comandos disponibles:
    /start - Inicia el bot
    /help - Muestra los comandos disponibles
    /add - Agrega un recordatorio
    /list - Muestra los recordatorios
    /delete - Elimina un recordatorio
    """)
    await message.answer(msg)


@router.message(Command("add"))
async def add_handler(message: Message, command: CommandObject):
    partes = command.args.split()
    if not command.args or len(partes) < 3:
        await message.answer("Uso: /add <fecha> <hora> <recordatorio>")
        return
    
    fecha_str = partes[0]
    hora_str = partes[1]
    recordatorio_texto = " ".join(partes[2:])
    
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()
        fecha_hora = datetime.combine(fecha, hora)
        ahora = datetime.now()

        if fecha_hora <= ahora:
            await message.answer("La fecha y hora deben ser posteriores a la actual")
            return
        
        global next_id
        recordatorios[next_id] = {
            "user_id": message.from_user.id,
            "fecha_hora": fecha_hora,
            "recordatorio": recordatorio_texto
        }
        msg = inspect.cleandoc("""
        ✅ Recordatorio guardado correctamente
        """)
        await message.answer(msg)
    except ValueError:
        await message.answer("Formato de fecha u hora inválido. Usa: dd/mm/yyyy HH:MM")
        return

