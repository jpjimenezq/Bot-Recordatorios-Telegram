import asyncpg

pool: asyncpg.Pool | None = None


async def conectar(url: str) -> None:
    global pool
    pool = await asyncpg.create_pool(url)
    await pool.execute("""
        CREATE TABLE IF NOT EXISTS recordatorios (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            texto TEXT NOT NULL,
            fecha_hora TIMESTAMPTZ NOT NULL,
            enviado BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)


async def desconectar() -> None:
    if pool:
        await pool.close()