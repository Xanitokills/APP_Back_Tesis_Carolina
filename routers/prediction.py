import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException
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

@router.post("/", response_model=schemas.Estilo, summary="Predice y devuelve datos del estilo de arte")
async def predict_style(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # 1) Guardar el archivo temporalmente
        temp_dir = "uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        print(f"Archivo guardado temporalmente en: {temp_path}")

        # 2) Verificar que el archivo se guardó correctamente
        if not os.path.isfile(temp_path):
            raise HTTPException(status_code=500, detail="Fallo al guardar el archivo temporal")

        # 3) Realizar la predicción
        nombre_estilo = predict_style_from_path(temp_path)
        if not nombre_estilo:
            raise HTTPException(status_code=500, detail="No se pudo predecir el estilo")

        # 4) Recuperar de la base de datos
        estilo = crud.get_estilo_por_nombre(db, nombre_estilo)
        if not estilo:
            raise HTTPException(status_code=404, detail=f"Estilo '{nombre_estilo}' no encontrado en la BD")

        # 5) Eliminar el archivo temporal
        os.remove(temp_path)
        print(f"Archivo temporal {temp_path} eliminado")

        return estilo

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error en predict_style: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Limpieza: Archivo {temp_path} eliminado")