from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import redis
from api import cv_endpoints
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="CV Generator API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True
)


@app.get("/")
async def root():
    try:
        logging.debug("Intentando conectar a Redis en %s:%s",
                      os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"))
        redis_client.ping()
        redis_status = "conectado"
        logging.debug("Conexión a Redis exitosa")
    except Exception as e:
        redis_status = "desconectado"
        logging.error("Error al conectar a Redis: %s", str(e))
    return {
        "message": "CV Generator API está funcionando!",
        "redis_status": redis_status
    }

# Incluir los endpoints de CV
app.include_router(cv_endpoints.router, prefix="/api")
