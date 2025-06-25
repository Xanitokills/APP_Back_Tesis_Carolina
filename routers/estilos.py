from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/estilos", tags=["estilos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Estilo)
def create_estilo(estilo: schemas.EstiloCreate, db: Session = Depends(get_db)):
    return crud.create_estilo(db, estilo)

@router.get("/", response_model=List[schemas.Estilo])
def read_estilos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_estilos(db, skip, limit)

@router.get("/{id}", response_model=schemas.Estilo)
def read_estilo(id: int, db: Session = Depends(get_db)):
    e = crud.get_estilo(db, id)
    if not e:
        raise HTTPException(status_code=404, detail="Estilo no encontrado")
    return e

@router.put("/{id}", response_model=schemas.Estilo)
def update_estilo(id: int, estilo: schemas.EstiloCreate, db: Session = Depends(get_db)):
    updated = crud.update_estilo(db, id, estilo)
    if not updated:
        raise HTTPException(status_code=404, detail="Estilo no encontrado")
    return updated

@router.delete("/{id}", response_model=schemas.Estilo)
def delete_estilo(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_estilo(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Estilo no encontrado")
    return deleted
