from fastapi import FastAPI
from .database import engine, Base
from .routers import estilos, prediction
import app.models  # noqa: fuerza registro de modelos

# Crea tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="APP GAAAAAA")

app.include_router(estilos.router)
app.include_router(prediction.router)
