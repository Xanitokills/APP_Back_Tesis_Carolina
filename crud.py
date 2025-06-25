from sqlalchemy.orm import Session
from . import models, schemas

def get_estilos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Estilo).offset(skip).limit(limit).all()

def get_estilo(db: Session, estilo_id: int):
    return db.query(models.Estilo).filter(models.Estilo.id == estilo_id).first()

def get_estilo_por_nombre(db: Session, nombre: str):
    return db.query(models.Estilo).filter(models.Estilo.nombre == nombre).first()

def create_estilo(db: Session, estilo_in: schemas.EstiloCreate):
    db_estilo = models.Estilo(**estilo_in.dict())
    db.add(db_estilo)
    db.commit()
    db.refresh(db_estilo)
    return db_estilo

def update_estilo(db: Session, estilo_id: int, estilo_in: schemas.EstiloCreate):
    estilo = get_estilo(db, estilo_id)
    if not estilo:
        return None
    for field, value in estilo_in.dict().items():
        setattr(estilo, field, value)
    db.commit()
    db.refresh(estilo)
    return estilo

def delete_estilo(db: Session, estilo_id: int):
    estilo = get_estilo(db, estilo_id)
    if not estilo:
        return None
    db.delete(estilo)
    db.commit()
    return estilo
