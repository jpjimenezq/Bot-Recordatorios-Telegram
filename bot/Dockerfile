FROM python:3.12-slim

# Copiamos uv desde su imagen oficial (gestor de dependencias del proyecto)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Primero solo las dependencias: si no cambian, Docker reutiliza esta capa en caché
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Después el código, que es lo que cambia más seguido
COPY . .

CMD ["python", "main.py"]
