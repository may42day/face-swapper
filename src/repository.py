from tortoise import Tortoise
import os


async def init_tortoise():
    db_url = os.getenv("DB_URL")
    await Tortoise.init(db_url=db_url, modules={"models": ["src.models"]})
    await Tortoise.generate_schemas()


async def close_tortoise():
    await Tortoise.close_connections()
