import pytest
import os
from unittest.mock import patch, MagicMock
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


@pytest.fixture
def full_cv_data():
    return {
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "+9876543210",
        "summary": "Full-stack developer",
        "experience": [
            {
                "company": "Web Inc",
                "position": "Lead Developer",
                "start_date": "2019-01-01",
                "end_date": "2023-06-30",
                "description": "Led frontend team",
                "location": "Austin",
                "achievements": ["Built design system", "Migrated to TypeScript"],
                "technologies": ["React", "TypeScript", "Node.js"],
            }
        ],
        "education": [
            {
                "institution": "Stanford",
                "degree": "BSc",
                "field_of_study": "Computer Science",
                "start_date": "2015-09-01",
                "end_date": "2019-06-15",
            }
        ],
        "skills": [
            {"name": "Python", "level": 5},
            {"name": "JavaScript", "level": 4},
        ],
        "certificates": [
            {
                "name": "AWS Developer",
                "issuer": "Amazon",
                "date_obtained": "2021-05-01",
            }
        ],
        "languages": [
            {"name": "English", "level": "Native"},
            {"name": "Spanish", "level": "Fluent"},
        ],
        "website": "https://jane.dev",
        "linkedin": "https://linkedin.com/in/jane",
        "github": "https://github.com/jane",
    }


def test_root_endpoint():
    from unittest.mock import patch

    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    with patch("web.backend.main.redis_client", mock_redis):
        response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["redis_status"] == "conectado"


def test_generate_cv(sample_cv_data):
    response = client.post("/api/cv/generate", json=sample_cv_data)
    assert response.status_code == 200
    assert "data" in response.json()


def test_generate_cv_invalid_data():
    response = client.post("/api/cv/generate", json={"full_name": "Test"})
    assert response.status_code == 422


def test_generate_cv_with_full_data(full_cv_data):
    response = client.post("/api/cv/generate", json=full_cv_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["full_name"] == "Jane Smith"
    assert len(data["experience"]) == 1
    assert len(data["education"]) == 1
    assert len(data["skills"]) == 2
    assert len(data["certificates"]) == 1
    assert len(data["languages"]) == 2


def test_generate_cv_missing_email():
    response = client.post("/api/cv/generate", json={"full_name": "Test"})
    assert response.status_code == 422


def test_generate_cv_invalid_email():
    response = client.post(
        "/api/cv/generate", json={"full_name": "Test", "email": "not-email"}
    )
    assert response.status_code == 422


def test_export_cv_pdf(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "pdf"}
    )
    assert response.status_code == 200


def test_export_cv_html(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "html"}
    )
    assert response.status_code == 200
    assert "data" in response.json()


def test_export_cv_markdown(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "md"}
    )
    assert response.status_code == 200
    assert "data" in response.json()


def test_export_cv_invalid_format(sample_cv_data):
    response = client.post(
        "/api/cv/export", json=sample_cv_data, params={"format": "invalid"}
    )
    assert response.status_code == 400


def test_get_templates():
    response = client.get("/api/cv/templates")
    assert response.status_code == 200
    assert isinstance(response.json()["templates"], list)
    templates = response.json()["templates"]
    assert "moderno" in templates
    assert "clásico" in templates
    assert "profesional" in templates


def test_list_cvs():
    response = client.get("/api/cv")
    assert response.status_code == 200


def test_upload_photo():
    test_photo_path = "tests/test_files/test_photo.jpg"
    if not os.path.exists(test_photo_path):
        os.makedirs(os.path.dirname(test_photo_path), exist_ok=True)
        with open(test_photo_path, "wb") as f:
            f.write(b"fake jpg content")

    with open(test_photo_path, "rb") as f:
        response = client.post(
            "/api/cv/upload-photo",
            files={"file": ("test_photo.jpg", f, "image/jpeg")},
        )
        assert response.status_code == 200
        assert "photo_url" in response.json()
        assert response.json()["photo_url"].startswith("data:image/jpeg;base64,")


def test_upload_photo_returns_base64():
    import base64

    img_content = b"\xff\xd8\xff\xe0test_image_data"
    test_photo_path = "tests/test_files/test_photo.jpg"
    os.makedirs(os.path.dirname(test_photo_path), exist_ok=True)
    with open(test_photo_path, "wb") as f:
        f.write(img_content)

    with open(test_photo_path, "rb") as f:
        response = client.post(
            "/api/cv/upload-photo",
            files={"file": ("test_photo.jpg", f, "image/jpeg")},
        )
    photo_url = response.json()["photo_url"]
    b64_part = photo_url.split("base64,")[1]
    decoded = base64.b64decode(b64_part)
    assert decoded == img_content


def test_get_cv_not_found():
    mock_redis = MagicMock()
    mock_redis.hgetall.return_value = {}
    with patch("web.backend.api.cv_endpoints.redis_client", mock_redis):
        response = client.get("/api/cv/nonexistent@example.com")
    assert response.status_code == 404


def test_get_cv_versions_not_found():
    mock_redis = MagicMock()
    mock_redis.lrange.return_value = []
    with patch("web.backend.api.cv_endpoints.redis_client", mock_redis):
        response = client.get("/api/cv/nobody@example.com/versions")
    assert response.status_code == 200
    assert response.json() == []
