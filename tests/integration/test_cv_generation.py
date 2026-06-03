import pytest
from fastapi.testclient import TestClient
from web.backend.main import app
from shared.services.cv_generator import CVGenerator
from shared.utils.cache import Cache
import os
from datetime import date


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def cv_generator():
    return CVGenerator()


@pytest.fixture
def cache():
    return Cache(host="localhost")


@pytest.fixture
def sample_cv_data():
    return {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "summary": "Experienced software engineer",
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Developer",
                "start_date": str(date(2020, 1, 1)),
                "end_date": str(date(2023, 12, 31)),
                "description": "Development of web applications",
            }
        ],
        "education": [],
        "skills": [],
        "certificates": [],
    }


@pytest.mark.asyncio
async def test_complete_cv_generation_flow(client, sample_cv_data):
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "data" in response.json()

    test_photo_path = "tests/test_files/test_photo.jpg"
    if not os.path.exists(test_photo_path):
        os.makedirs(os.path.dirname(test_photo_path), exist_ok=True)
        with open(test_photo_path, "wb") as f:
            f.write(b"fake jpg content")

    with open(test_photo_path, "rb") as f:
        response = client.post(
            "/api/cv/upload-photo", files={"file": ("test_photo.jpg", f, "image/jpeg")}
        )
        assert response.status_code == 200
        assert "photo_url" in response.json()


@pytest.mark.asyncio
async def test_error_handling(client):
    response = client.post("/api/cv/generate", json={"full_name": "Test"})
    assert response.status_code == 422

    response = client.post(
        "/api/cv/export",
        json={"full_name": "Test", "email": "test@example.com"},
        params={"format": "invalid"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_template_management(client, cv_generator):
    response = client.get("/api/cv/templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert isinstance(templates, list)
    assert len(templates) > 0
