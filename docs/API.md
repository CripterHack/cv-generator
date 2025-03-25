# API Documentation

## Overview

The CV Generator API provides endpoints for creating, managing, and exporting CVs. The API is built with FastAPI and provides automatic OpenAPI documentation.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API is open and doesn't require authentication.

## Endpoints

### CV Generation

#### Generate CV
```http
POST /api/cv/generate
```

Generates a CV from the provided data.

**Request Body:**
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

**Response:**
```json
{
  "html": "string"
}
```

#### Export CV
```http
POST /api/cv/export
```

Exports CV in the specified format.

**Query Parameters:**
- `format`: string (pdf, html, md)

**Request Body:** Same as Generate CV

**Response:**
- PDF format: Binary file
- HTML format: HTML string
- Markdown format: Markdown string

### Photo Management

#### Upload Photo
```http
POST /api/cv/upload-photo
```

Upload a photo for the CV.

**Request Body:**
- `file`: binary (multipart/form-data)

**Response:**
```json
{
  "photo_url": "string"
}
```

### Templates

#### Get Available Templates
```http
GET /api/cv/templates
```

Returns a list of available CV templates.

**Response:**
```json
{
  "templates": ["string"]
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

Error responses include a message:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per IP

## CORS

The API has CORS enabled to allow requests from `http://localhost:3000` in development and from configured domains in production.

## Detailed Error Responses

The API provides detailed error responses in the following format:

- 400: Bad Request
  ```json
  {
    "detail": "Invalid file format. Supported formats: jpg, png"
  }
  ```

- 413: Payload Too Large
  ```json
  {
    "detail": "File size exceeds maximum limit of 5MB"
  }
  ```

- 422: Validation Error
  ```json
  {
    "detail": {
      "field": ["validation error message"]
    }
  }
  ```

## Interactive Documentation

Full interactive API documentation is available at `/docs` when running the server:

1. Start the server:
   ```bash
   ./dev.sh start
   ```

2. Visit:
   ```
   http://localhost:8000/docs
   ```

## Examples

### Generate CV
```bash
curl -X POST http://localhost:8000/api/cv/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "title": "Software Engineer",
    "professional_experience": []
  }'
```

### Export as PDF
```bash
curl -X POST http://localhost:8000/api/cv/export?format=pdf \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "title": "Software Engineer",
    "professional_experience": []
  }' \
  --output cv.pdf
``` 