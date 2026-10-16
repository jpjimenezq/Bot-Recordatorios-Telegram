# Bot de recordatorios de Telegram

Bot de Telegram para guardar recordatorios con fecha y hora. Está hecho con [aiogram](https://docs.aiogram.dev/) 3 y PostgreSQL, y corre en Docker con Docker Compose.

## Estado actual

Por ahora el bot **solo almacena los recordatorios**. Puedes crearlos, verlos y borrarlos, pero todavía no te avisa cuando llega la hora.

Más adelante se agregará el envío automático de recordatorios (por ejemplo, un aviso 5 minutos antes).

## Comandos

| Comando | Descripción |
| --- | --- |
| `/inicio` | Inicia el bot |
| `/ayuda` | Muestra los comandos disponibles |
| `/agregar <dd/mm/yyyy> <HH:MM> <texto>` | Guarda un recordatorio |
| `/listar` | Muestra tus recordatorios |
| `/borrar <id>` | Elimina un recordatorio por su id |

Ejemplo:

```
/agregar 02/06/2027 12:00 Cumpleaños
```

## Requisitos

- Docker y Docker Compose
- Un token de bot de Telegram (se consigue con [@BotFather](https://t.me/BotFather))

## Configuración

Crea un archivo `.env` en la raíz del proyecto, basándote en `.env.example`, con tus datos:

```
TELEGRAM_BOT_TOKEN=tu_token
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
```

El archivo `.env` no se sube al repositorio, así que nunca compartas tu token.

## Ejecutar

```bash
docker compose up -d --build
docker compose logs -f bot
```

Para detener los servicios:

```bash
docker compose down
```

## Estructura

```
.
├── docker-compose.yml   # Servicios: base de datos (db) y bot
├── .env.example         # Plantilla de variables de entorno
├── .gitignore
├── README.md
└── bot/
    ├── Dockerfile       # Imagen del bot
    ├── .dockerignore    # Archivos que no entran a la imagen
    ├── pyproject.toml   # Dependencias del proyecto (uv)
    ├── uv.lock         # Versiones exactas de las dependencias
    ├── main.py          # Arranque del bot
    └── src/
        ├── config.py        # Variables de entorno y zona horaria
        ├── database.py      # Conexión a PostgreSQL y creación de la tabla
        ├── handlers.py      # Comandos de Telegram
        └── repositories.py  # Consultas a la base de datos
```

`bot/requirements.txt` está vacío y no se usa, porque las dependencias se manejan con `uv`.
