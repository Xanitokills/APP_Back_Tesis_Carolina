from sqlalchemy import Column, Integer, String
from .database import Base

class Estilo(Base):
    __tablename__ = "estilos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False, unique=True, index=True)
    descripcion = Column(String, nullable=False)
    tecnicas = Column(String, nullable=False)
