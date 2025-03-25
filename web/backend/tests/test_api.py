import pytest
from fastapi.testclient import TestClient
from web.backend.main import app
from datetime import date

client = TestClient(app)

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
        ]
    }

def test_generate_cv(sample_cv_data):
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "html" in response.json()

def test_generate_cv_invalid_data():
    response = client.post("/api/cv/generate", json={})
    assert response.status_code == 422

def test_export_cv_pdf(sample_cv_data):
    response = client.post("/api/cv/export", json=sample_cv_data, params={"format": "pdf"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_export_cv_invalid_format(sample_cv_data):
    response = client.post("/api/cv/export", json=sample_cv_data, params={"format": "invalid"})
    assert response.status_code == 400

def test_get_templates():
    response = client.get("/api/cv/templates")
    assert response.status_code == 200
    assert isinstance(response.json()["templates"], list)

def test_upload_photo():
    with open("tests/test_files/test_photo.jpg", "rb") as f:
        response = client.post(
            "/api/cv/upload-photo",
            files={"file": ("test_photo.jpg", f, "image/jpeg")}
        )
        assert response.status_code == 200
        assert "photo_url" in response.json() 