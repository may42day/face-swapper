from src.utils import init_detecting_model
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

# The initial run initiates the download of buffalo_l to .insightface\models\
from insightface.app import FaceAnalysis

FaceAnalysis(name="buffalo_l")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.repository import init_tortoise, close_tortoise

    await init_tortoise()
    yield
    await close_tortoise()


load_dotenv()
app = FastAPI(lifespan=lifespan)

from src.router import router

app.include_router(router)
