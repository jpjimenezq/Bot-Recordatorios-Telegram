import inspect

from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from src import repositories

# Zona horaria del usuario: las fechas se guardan con esta zona y se muestran en ella
ZONA = ZoneInfo("America/Bogota")

# Lista de comandos; se usa en /ayuda y cuando el usuario escribe algo que no entendemos
AYUDA = inspect.cleandoc("""
    Comandos disponibles:
    /inicio - Inicia el bot
    /ayuda - Muestra los comandos disponibles
    /agregar - Agrega un recordatorio
    /listar - Muestra los recordatorios
    /borrar - Elimina un recordatorio
    """)

router = Router()

@router.message(Command("inicio", "start"))
async def start_handler(message: Message):
    msg = inspect.cleandoc("""
    ¡Hola! Soy tu bot de recordatorios.
    Puedo ayudarte a guardar y recibir recordatorios.
    """)
    await message.answer(msg)


@router.message(Command("ayuda"))
async def help_handler(message: Message):
    await message.answer(AYUDA)


@router.message(Command("agregar"))
async def add_handler(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Uso: /agregar <fecha> <hora> <recordatorio>")
        return
    
    partes = command.args.split()
    if len(partes) < 3:
        await message.answer("Uso: /agregar <fecha> <hora> <recordatorio>")
        return

    fecha_str = partes[0]
    hora_str = partes[1]
    recordatorio_texto = " ".join(partes[2:])
    
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()
        fecha_hora = datetime.combine(fecha, hora, tzinfo=ZONA)
        ahora = datetime.now(ZONA)

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
        local = fila["fecha_hora"].astimezone(ZONA)
        msg += f"\n{fila['id']}. {fila['texto']} - {local:%d/%m/%Y %H:%M}"
    await message.answer(msg)


@router.message(Command("borrar"))
async def delete_handler(message: Message, command: CommandObject):
    try:
        await repositories.borrar(int(command.args))
        await message.answer("✅ Recordatorio eliminado correctamente")
    except (TypeError, ValueError, IndexError):
        await message.answer("Uso: /borrar <id>")
    except Exception as e:
        await message.answer(f"Error: {e}")


@router.message()
async def mensaje_desconocido(message: Message):
    await message.answer("No entendí ese mensaje.\n\n" + AYUDA)

