import pytest
import os
from datetime import date
from shared.services.cv_generator import CVGenerator, CVGenerationError

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'templates')

@pytest.fixture
def cv_generator():
    return CVGenerator()

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

async def test_generate_cv(cv_generator, sample_cv_data):
    result = await cv_generator.generate(sample_cv_data)
    assert "html" in result
    assert sample_cv_data["name"] in result["html"]

def test_get_available_templates(cv_generator):
    templates = cv_generator.get_available_templates()
    assert isinstance(templates, list)
    assert all(t.endswith(".html") for t in templates)

async def test_export_cv_invalid_format(cv_generator, sample_cv_data):
    with pytest.raises(ValueError):
        await cv_generator.export(sample_cv_data, "invalid_format") 