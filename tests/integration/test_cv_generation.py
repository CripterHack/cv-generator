import pytest
from fastapi.testclient import TestClient
from web.backend.main import app
from shared.services.cv_generator import CVGenerator
from shared.utils.cache import Cache
import os
import json
from datetime import date

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def cv_generator():
    return CVGenerator()

@pytest.fixture
def cache():
    return Cache(host='redis')

@pytest.fixture
def sample_cv_data():
    return {
        "name": "John Doe",
        "title": "Software Engineer",
        "phone": "+1234567890",
        "age": 30,
        "city": "New York",
        "summary": "Experienced software engineer",
        "professional_experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Developer",
                "start_date": str(date(2020, 1, 1)),
                "end_date": str(date(2023, 12, 31)),
                "description": "Development of web applications"
            }
        ],
        "academic_experience": [],
        "skills": ["Python", "JavaScript", "React"],
        "certificates": []
    }

@pytest.mark.asyncio
async def test_complete_cv_generation_flow(client, sample_cv_data, cache):
    # Test CV generation
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "html" in response.json()
    
    # Verify cache is working
    cache_key = f"generate_cv:{json.dumps(sample_cv_data)}"
    cached_result = cache.get(cache_key)
    assert cached_result is not None
    
    # Test PDF export
    response = client.post(
        "/api/cv/export",
        json=sample_cv_data,
        params={"format": "pdf"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    
    # Test photo upload
    test_photo_path = "tests/test_files/test_photo.jpg"
    if not os.path.exists(test_photo_path):
        os.makedirs(os.path.dirname(test_photo_path), exist_ok=True)
        with open(test_photo_path, "wb") as f:
            f.write(b"test photo content")
    
    with open(test_photo_path, "rb") as f:
        response = client.post(
            "/api/cv/upload-photo",
            files={"file": ("test_photo.jpg", f, "image/jpeg")}
        )
        assert response.status_code == 200
        assert "photo_url" in response.json()
        photo_url = response.json()["photo_url"]
    
    # Test CV generation with photo
    sample_cv_data["photo_base64"] = photo_url
    sample_cv_data["show_photo"] = True
    
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "html" in response.json()
    assert photo_url in response.json()["html"]

@pytest.mark.asyncio
async def test_error_handling(client):
    # Test invalid CV data
    response = client.post("/api/cv/generate", json={})
    assert response.status_code == 422
    
    # Test invalid export format
    response = client.post(
        "/api/cv/export",
        json={"name": "Test"},
        params={"format": "invalid"}
    )
    assert response.status_code == 400
    
    # Test invalid photo upload
    response = client.post(
        "/api/cv/upload-photo",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_template_management(client, cv_generator):
    # Get available templates
    response = client.get("/api/cv/templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert isinstance(templates, list)
    assert len(templates) > 0
    
    # Verify each template exists
    for template in templates:
        assert template.endswith(".html")
        assert template in os.listdir(cv_generator.template_env.loader.searchpath[0]) 