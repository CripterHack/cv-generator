from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from typing import List, Optional
from ..models.cv import CV
import base64
import os
from pathlib import Path
from datetime import datetime
import redis
import json
from ..services.export_service import ExportService

router = APIRouter()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)


@router.post("/cv/")
async def create_cv(cv: CV):
    try:
        # Agregar timestamps
        cv.created_at = datetime.now()
        cv.updated_at = datetime.now()

        # Guardar en Redis
        cv_data = cv.dict()
        cv_key = f"cv:{cv.email}"
        redis_client.hset(cv_key, mapping=cv_data)

        # Guardar versión
        version_key = f"cv_versions:{cv.email}"
        redis_client.rpush(version_key, json.dumps(cv_data))

        return cv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv/{email}")
async def get_cv(email: str, version: Optional[int] = None):
    try:
        if version:
            # Obtener versión específica
            version_key = f"cv_versions:{email}"
            versions = redis_client.lrange(version_key, 0, -1)
            if version <= len(versions):
                cv_data = json.loads(versions[version - 1])
                return CV(**cv_data)
            raise HTTPException(status_code=404, detail="Version not found")

        # Obtener versión actual
        cv_key = f"cv:{email}"
        cv_data = redis_client.hgetall(cv_key)
        if not cv_data:
            raise HTTPException(status_code=404, detail="CV not found")
        return CV(**cv_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/cv/{email}")
async def update_cv(email: str, cv: CV):
    try:
        # Verificar existencia
        cv_key = f"cv:{email}"
        if not redis_client.exists(cv_key):
            raise HTTPException(status_code=404, detail="CV not found")

        # Actualizar timestamps
        cv.updated_at = datetime.now()

        # Incrementar versión
        cv.version = cv.version + 1 if cv.version else 1

        # Guardar en Redis
        cv_data = cv.dict()
        redis_client.hset(cv_key, mapping=cv_data)

        # Guardar nueva versión
        version_key = f"cv_versions:{email}"
        redis_client.rpush(version_key, json.dumps(cv_data))

        return cv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv/{email}/versions")
async def get_cv_versions(email: str):
    try:
        version_key = f"cv_versions:{email}"
        versions = redis_client.lrange(version_key, 0, -1)
        return [json.loads(v) for v in versions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cv/{email}/photo")
async def upload_photo(email: str, file: UploadFile = File(...)):
    try:
        # Implementar lógica de guardado de foto
        # Actualizar CV con URL de la foto
        return {"message": "Photo uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cv/generate")
async def generate_cv(cv_data: CV):
    """
    Generate a CV from the provided data.
    """
    try:
        return {
            "message": "CV generado exitosamente",
            "data": cv_data.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cv/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    """
    Upload a photo for the CV.
    """
    try:
        contents = await file.read()
        # Convertir la imagen a base64
        base64_image = base64.b64encode(contents).decode()
        return {"photo_url": f"data:image/{file.content_type};base64,{base64_image}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cv/export")
async def export_cv(cv_data: CV, format: str = "pdf"):
    """
    Export CV in the specified format.
    """
    try:
        if format not in ["pdf", "html", "md"]:
            raise HTTPException(status_code=400, detail="Formato no soportado")

        return {
            "message": f"CV exportado en formato {format}",
            "data": cv_data.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv/templates")
async def get_templates():
    """
    Get available CV templates.
    """
    try:
        templates = ["moderno", "clásico", "profesional"]
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv")
async def get_cv():
    return {"message": "CV endpoint"}


@router.get("/cv/{email}/export/pdf")
async def export_cv_to_pdf(email: str):
    try:
        cv_key = f"cv:{email}"
        cv_data = redis_client.hgetall(cv_key)
        if not cv_data:
            raise HTTPException(status_code=404, detail="CV not found")

        cv = CV(**cv_data)
        pdf_path = await ExportService.to_pdf(cv)
        return {"pdf_url": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv/{email}/export/markdown")
async def export_cv_to_markdown(email: str):
    try:
        cv_key = f"cv:{email}"
        cv_data = redis_client.hgetall(cv_key)
        if not cv_data:
            raise HTTPException(status_code=404, detail="CV not found")

        cv = CV(**cv_data)
        markdown_content = await ExportService.to_markdown(cv)
        return {"content": markdown_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
