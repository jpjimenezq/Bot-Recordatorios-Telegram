import inspect

from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from src import repositories

router = Router()

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
        
        id_recordatorio = await repositories.agregar(
            message.from_user.id, 
            recordatorio_texto, 
            fecha_hora
        )
        msg = inspect.cleandoc("""
        ✅ Recordatorio guardado correctamente
        """)
        await message.answer(msg)
    except ValueError:
        await message.answer("Formato de fecha u hora inválido. Usa: dd/mm/yyyy HH:MM")
        return


@router.message(Command("listar"))
async def list_handler(message: Message):
    filas = await repositories.listar(message.from_user.id)
    if not filas:
        await message.answer("No hay recordatorios")
        return
    
    msg = inspect.cleandoc("""
    📋 Tus recordatorios:
    """)
    for fila in filas:
        msg += f"\n{fila['id']}. {fila['texto']} - {fila['fecha_hora']}"
    await message.answer(msg)


@router.message(Command("borrar"))
async def delete_handler(message: Message, command: CommandObject):
    try:
        await repositories.borrar(int(command.args))
        await message.answer("✅ Recordatorio eliminado correctamente")
    except (ValueError, IndexError):
        await message.answer("Uso: /borrar <id>")
    except Exception as e:
        await message.answer(f"Error: {e}")
        
