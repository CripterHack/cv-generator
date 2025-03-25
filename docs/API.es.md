# Documentación de la API

## Descripción General

La API del Generador de CV proporciona endpoints para crear, gestionar y exportar CVs. La API está construida con FastAPI y proporciona documentación OpenAPI automática.

## URL Base

```
http://localhost:8000
```

## Autenticación

Actualmente, la API es abierta y no requiere autenticación.

## Endpoints

### Generación de CV

#### Generar CV
```http
POST /api/cv/generate
```

Genera un CV a partir de los datos proporcionados.

**Cuerpo de la Petición:**
```json
{
  "name": "string",
  "title": "string",
  "phone": "string",
  "age": 0,
  "city": "string",
  "summary": "string",
  "photo_base64": "string",
  "show_photo": true,
  "professional_experience": [
    {
      "company": "string",
      "position": "string",
      "start_date": "2023-01-01",
      "end_date": "2023-12-31",
      "description": "string"
    }
  ],
  "academic_experience": [
    {
      "institution": "string",
      "degree": "string",
      "start_date": "2023-01-01",
      "end_date": "2023-12-31"
    }
  ],
  "skills": ["string"],
  "certificates": [
    {
      "name": "string",
      "institution": "string",
      "date": "2023-01-01"
    }
  ]
}
```

**Respuesta:**
```json
{
  "html": "string"
}
```

#### Exportar CV
```http
POST /api/cv/export
```

Exporta el CV en el formato especificado.

**Parámetros de Consulta:**
- `format`: string (pdf, html, md)

**Cuerpo de la Petición:** Igual que Generar CV

**Respuesta:**
- Formato PDF: Archivo binario
- Formato HTML: Cadena HTML
- Formato Markdown: Cadena Markdown

### Gestión de Fotos

#### Subir Foto
```http
POST /api/cv/upload-photo
```

Sube una foto para el CV.

**Cuerpo de la Petición:**
- `file`: binario (multipart/form-data)

**Respuesta:**
```json
{
  "photo_url": "string"
}
```

### Plantillas

#### Obtener Plantillas Disponibles
```http
GET /api/cv/templates
```

Devuelve una lista de plantillas de CV disponibles.

**Respuesta:**
```json
{
  "templates": ["string"]
}
```

## Manejo de Errores

La API utiliza códigos de estado HTTP estándar:

- 200: Éxito
- 400: Solicitud Incorrecta
- 404: No Encontrado
- 422: Error de Validación
- 500: Error Interno del Servidor

Las respuestas de error incluyen un mensaje:
```json
{
  "detail": "Mensaje de error"
}
```

## Límites de Tasa

- 100 solicitudes por minuto por IP
- 1000 solicitudes por hora por IP

## CORS

La API tiene habilitado CORS para permitir peticiones desde `http://localhost:3000` en desarrollo y desde los dominios configurados en producción.

## Respuestas de Error Detalladas

La API proporciona respuestas de error detalladas en el siguiente formato:

- 400: Solicitud Incorrecta
  ```json
  {
    "detail": "Formato de archivo inválido. Formatos soportados: jpg, png"
  }
  ```

- 413: Carga Demasiado Grande
  ```json
  {
    "detail": "El tamaño del archivo excede el límite máximo de 5MB"
  }
  ```

- 422: Error de Validación
  ```json
  {
    "detail": {
      "campo": ["mensaje de error de validación"]
    }
  }
  ```

## Documentación Interactiva

La documentación completa e interactiva de la API está disponible en `/docs` cuando el servidor está en ejecución:

1. Iniciar el servidor:
   ```bash
   ./dev.sh start
   ```

2. Visitar:
   ```
   http://localhost:8000/docs
   ```

## Ejemplos

### Generar CV
```bash
curl -X POST http://localhost:8000/api/cv/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "title": "Ingeniero de Software",
    "professional_experience": []
  }'
```

### Exportar como PDF
```bash
curl -X POST http://localhost:8000/api/cv/export?format=pdf \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "title": "Ingeniero de Software",
    "professional_experience": []
  }' \
  --output cv.pdf
``` 