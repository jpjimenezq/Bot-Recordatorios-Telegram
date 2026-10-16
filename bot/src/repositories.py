import datetime
from src import database

async def agregar(chat_id: int, texto: str, fecha_hora: datetime.datetime) -> int:
    fila = await database.pool.fetchrow(
        "INSERT INTO recordatorios(chat_id, texto, fecha_hora)"
        "VALUES ($1, $2, $3) RETURNING id"
        , chat_id, texto, fecha_hora
    )
    return fila["id"]


async def listar(chat_id: int) -> list[dict[str, object]]:
    filas = await database.pool.fetch(
        "SELECT * FROM recordatorios WHERE chat_id = $1"
        , chat_id
    )
    return [dict(fila) for fila in filas]


async def borrar(id: int) -> None:
    await database.pool.execute(
        "DELETE FROM recordatorios WHERE id = $1"
        , id
    )