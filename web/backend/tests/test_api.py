import pytest
import os
from fastapi.testclient import TestClient
from web.backend.main import app
from datetime import date

client = TestClient(app)


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
    }


def test_generate_cv(sample_cv_data):
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "data" in response.json()


def test_generate_cv_invalid_data():
    response = client.post("/api/cv/generate", json={"full_name": "Test"})
    assert response.status_code == 422


def test_export_cv_pdf(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "pdf"}
    )
    assert response.status_code == 200


def test_export_cv_invalid_format(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "invalid"}
    )
    assert response.status_code == 400


def test_get_templates():
    response = client.get("/api/cv/templates")
    assert response.status_code == 200
    assert isinstance(response.json()["templates"], list)


def test_upload_photo():
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
