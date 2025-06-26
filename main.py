from fastapi import FastAPI
from .database import engine, Base
from .routers import estilos, prediction
import app.models  # noqa: fuerza registro de modelos

# Crea tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="APP GAAAAAAaaaa")

app.include_router(estilos.router)
app.include_router(prediction.router)

# Inicia el servidor uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Ajustado al puerto 8000 para coincidir con el túnel