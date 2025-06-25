import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from ..ml_model import predict_style_from_path

router = APIRouter(prefix="/predict", tags=["prediction"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class PathInput(BaseModel):
    path: str

@router.post("/", response_model=schemas.Estilo, summary="Predice y devuelve datos del estilo de arte")
def predict_style(input: PathInput, db: Session = Depends(get_db)):
    # 1) Comprueba existencia de fichero
    if not os.path.isfile(input.path):
        raise HTTPException(status_code=400, detail="El path de la imagen no existe")
    # 2) Predicción
    try:
        nombre_estilo = predict_style_from_path(input.path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")
    # 3) Recupera de BD
    e = crud.get_estilo_por_nombre(db, nombre_estilo)
    if not e:
        raise HTTPException(status_code=404, detail=f"Estilo '{nombre_estilo}' no encontrado en la BD")
    return e
