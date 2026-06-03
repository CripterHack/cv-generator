import pytest
import os
from datetime import date
from unittest.mock import patch
from shared.services.cv_generator import CVGenerator, CVGenerationError

TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "shared", "templates"
)


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
                "description": "Development of web applications",
            }
        ],
    }


@pytest.mark.asyncio
async def test_generate_cv(cv_generator, sample_cv_data):
    result = await cv_generator.generate(sample_cv_data)
    assert "html" in result
    assert sample_cv_data["name"] in result["html"]


def test_get_available_templates(cv_generator):
    templates = cv_generator.get_available_templates()
    assert isinstance(templates, list)
    assert all(t.endswith(".html") for t in templates)
    assert "cv_template.html" in templates


@pytest.mark.asyncio
async def test_export_cv_invalid_format(cv_generator, sample_cv_data):
    with pytest.raises(ValueError):
        await cv_generator.export(sample_cv_data, "invalid_format")


@pytest.mark.asyncio
async def test_export_cv_html(cv_generator, sample_cv_data):
    result = await cv_generator.export(sample_cv_data, "html")
    assert "html" in result
    assert sample_cv_data["name"] in result["html"]


@pytest.mark.asyncio
async def test_export_cv_pdf(cv_generator, sample_cv_data):
    with patch("shared.services.cv_generator.pdfkit") as mock_pdfkit:
        mock_pdfkit.from_string.return_value = b"fake pdf bytes"
        result = await cv_generator.export(sample_cv_data, "pdf")
        assert "pdf" in result
        mock_pdfkit.from_string.assert_called_once()


@pytest.mark.asyncio
async def test_export_cv_markdown(cv_generator, sample_cv_data):
    with patch("shared.services.cv_generator.markdown2") as mock_md:
        mock_md.markdown.return_value = "<p>Test markdown</p>"
        result = await cv_generator.export(sample_cv_data, "md")
        assert "markdown" in result
        mock_md.markdown.assert_called_once()


@pytest.mark.asyncio
async def test_process_photo_none(cv_generator):
    result = await cv_generator._process_photo(None, "test.png")
    assert result is None


@pytest.mark.asyncio
async def test_process_photo_valid(cv_generator):
    with patch.object(
        cv_generator.file_handler, "save_photo", return_value="uploads/test.png"
    ):
        result = await cv_generator._process_photo("base64data", "test.png")
        assert result == "uploads/test.png"


@pytest.mark.asyncio
async def test_process_photo_error(cv_generator):
    with patch.object(
        cv_generator.file_handler, "save_photo", side_effect=Exception("disk full")
    ):
        with pytest.raises(CVGenerationError, match="Error processing photo"):
            await cv_generator._process_photo("base64data", "test.png")


@pytest.mark.asyncio
async def test_generate_cv_template_error(cv_generator):
    with patch.object(
        cv_generator.template_env,
        "get_template",
        side_effect=Exception("template not found"),
    ):
        with pytest.raises(CVGenerationError, match="Error generating CV"):
            await cv_generator.generate({"name": "Test"})


def test_get_available_templates_error(cv_generator):
    with patch("os.listdir", side_effect=OSError("permission denied")):
        with pytest.raises(CVGenerationError, match="Error getting templates"):
            cv_generator.get_available_templates()
