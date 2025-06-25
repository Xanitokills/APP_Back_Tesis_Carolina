from pydantic import BaseModel

class EstiloBase(BaseModel):
    id: int
    nombre: str
    descripcion: str
    tecnicas: str

class EstiloCreate(EstiloBase):
    pass

class Estilo(EstiloBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
