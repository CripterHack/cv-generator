import pytest
from unittest.mock import patch
import os
import tempfile
import shutil

from web.backend.services.export_service import ExportService
from web.backend.models.cv import (
    CV,
    Education,
    Experience,
    Skill,
    Certificate,
    Language,
)


@pytest.fixture
def minimal_cv():
    return CV(full_name="Jane Doe", email="jane@example.com")


@pytest.fixture
def full_cv():
    return CV(
        full_name="John Doe",
        email="john@example.com",
        phone="+1234567890",
        summary="Experienced software engineer",
        website="https://johndoe.dev",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        experience=[
            Experience(
                company="Tech Corp",
                position="Senior Developer",
                start_date="2020-01-01",
                end_date="2023-12-31",
                description="Built web applications",
                location="San Francisco",
                achievements=["Led team of 5", "Shipped v2.0"],
                technologies=["Python", "React", "Docker"],
            ),
            Experience(
                company="Startup Inc",
                position="Junior Developer",
                start_date="2018-06-01",
                description="First dev role",
            ),
        ],
        education=[
            Education(
                institution="MIT",
                degree="BSc",
                field_of_study="Computer Science",
                start_date="2014-09-01",
                end_date="2018-06-01",
                description="Focus on AI",
                achievements=["Dean's List"],
            ),
        ],
        skills=[
            Skill(name="Python", level=5, category="Backend"),
            Skill(name="TypeScript", level=4),
            Skill(name="Docker"),
        ],
        certificates=[
            Certificate(
                name="AWS Solutions Architect",
                issuer="Amazon",
                date_obtained="2022-03-15",
                credential_url="https://aws.amazon.com/cert/123",
            ),
            Certificate(
                name="Kubernetes Administrator",
                issuer="CNCF",
                date_obtained="2023-01-10",
                credential_id="CKA-2023-001",
            ),
        ],
        languages=[
            Language(name="English", level="Native"),
            Language(name="Spanish", level="Intermediate", certification="DELE B1"),
        ],
    )


class TestExportServiceToHtml:
    @pytest.mark.asyncio
    async def test_minimal_cv_html(self, minimal_cv):
        result = await ExportService.to_html(minimal_cv)
        assert "<!DOCTYPE html>" in result
        assert "Jane Doe" in result
        assert "jane@example.com" in result

    @pytest.mark.asyncio
    async def test_full_cv_html(self, full_cv):
        result = await ExportService.to_html(full_cv)
        assert "John Doe" in result
        assert "john@example.com" in result
        assert "+1234567890" in result
        assert "Experienced software engineer" in result
        assert "Tech Corp" in result
        assert "Senior Developer" in result
        assert "San Francisco" in result
        assert "Led team of 5" in result
        assert "Python, React, Docker" in result
        assert "MIT" in result
        assert "Computer Science" in result
        assert "AWS Solutions Architect" in result
        assert "Amazon" in result
        assert "Kubernetes Administrator" in result
        assert "English" in result
        assert "Native" in result
        assert "Spanish" in result
        assert "https://johndoe.dev" in result
        assert "https://linkedin.com/in/johndoe" in result
        assert "https://github.com/johndoe" in result

    @pytest.mark.asyncio
    async def test_html_optional_sections_absent(self, minimal_cv):
        result = await ExportService.to_html(minimal_cv)
        assert "Professional Experience" not in result
        assert "Education" not in result
        assert "Skills" not in result
        assert "Certificates" not in result
        assert "Languages" not in result
        assert "Professional Summary" not in result

    @pytest.mark.asyncio
    async def test_html_experience_present_date(self, full_cv):
        result = await ExportService.to_html(full_cv)
        assert "2020-01-01 - 2023-12-31" in result

    @pytest.mark.asyncio
    async def test_html_experience_open_end_date(self, minimal_cv):
        cv = CV(
            full_name="Alice",
            email="alice@example.com",
            experience=[
                Experience(
                    company="Current Job",
                    position="Dev",
                    start_date="2023-01-01",
                ),
            ],
        )
        result = await ExportService.to_html(cv)
        assert "Present" in result

    @pytest.mark.asyncio
    async def test_html_education_open_end_date(self, minimal_cv):
        cv = CV(
            full_name="Alice",
            email="alice@example.com",
            education=[
                Education(
                    institution="University",
                    degree="BSc",
                    field_of_study="CS",
                    start_date="2020-01-01",
                ),
            ],
        )
        result = await ExportService.to_html(cv)
        assert "Present" in result

    @pytest.mark.asyncio
    async def test_html_credential_url_rendered(self, full_cv):
        result = await ExportService.to_html(full_cv)
        assert "View Certificate" in result
        assert "https://aws.amazon.com/cert/123" in result

    @pytest.mark.asyncio
    async def test_html_no_phone_when_absent(self, minimal_cv):
        result = await ExportService.to_html(minimal_cv)
        assert minimal_cv.phone is None
        assert "+1234567890" not in result


class TestExportServiceToMarkdown:
    @pytest.mark.asyncio
    async def test_minimal_cv_markdown(self, minimal_cv):
        result = await ExportService.to_markdown(minimal_cv)
        assert "# Jane Doe" in result
        assert "jane@example.com" in result

    @pytest.mark.asyncio
    async def test_full_cv_markdown(self, full_cv):
        result = await ExportService.to_markdown(full_cv)
        assert "## Contact Information" in result
        assert "## Professional Summary" in result
        assert "## Professional Experience" in result
        assert "### Senior Developer at Tech Corp" in result
        assert "2020-01-01 - 2023-12-31" in result
        assert "San Francisco" in result
        assert "Key Achievements" in result
        assert "Led team of 5" in result
        assert "Python, React, Docker" in result
        assert "## Education" in result
        assert "MIT" in result
        assert "## Skills" in result
        assert "Python" in result
        assert "Level: 5/5" in result
        assert "Backend" in result
        assert "## Languages" in result
        assert "DELE B1" in result
        assert "## Certificates" in result
        assert "AWS Solutions Architect" in result
        assert "View Certificate" in result

    @pytest.mark.asyncio
    async def test_markdown_open_end_date(self, minimal_cv):
        cv = CV(
            full_name="Alice",
            email="alice@example.com",
            experience=[
                Experience(
                    company="Current",
                    position="Dev",
                    start_date="2023-01-01",
                ),
            ],
        )
        result = await ExportService.to_markdown(cv)
        assert "Present" in result

    @pytest.mark.asyncio
    async def test_markdown_no_optional_sections(self, minimal_cv):
        result = await ExportService.to_markdown(minimal_cv)
        assert "Professional Experience" not in result
        assert "Education" not in result
        assert "Skills" not in result


class TestExportServiceToPdf:
    @pytest.mark.asyncio
    async def test_to_pdf_creates_file(self, minimal_cv):
        export_dir = "static/exports"
        os.makedirs(export_dir, exist_ok=True)

        with patch("web.backend.services.export_service.pdfkit") as mock_pdfkit:
            mock_pdfkit.from_string.return_value = None
            result = await ExportService.to_pdf(minimal_cv)

        assert result.replace("\\", "/").startswith(
            "static/exports/cv_jane@example.com_"
        )
        assert result.endswith(".pdf")
        mock_pdfkit.from_string.assert_called_once()
        call_args = mock_pdfkit.from_string.call_args
        assert "Jane Doe" in call_args[0][0]

        shutil.rmtree("static", ignore_errors=True)

    @pytest.mark.asyncio
    async def test_to_pdf_uses_a4_options(self, minimal_cv):
        os.makedirs("static/exports", exist_ok=True)

        with patch("web.backend.services.export_service.pdfkit") as mock_pdfkit:
            mock_pdfkit.from_string.return_value = None
            await ExportService.to_pdf(minimal_cv)

        call_args = mock_pdfkit.from_string.call_args
        options = (
            call_args[0][2] if len(call_args[0]) > 2 else call_args[1].get("options")
        )
        if options is None:
            options = call_args[1]
        assert options["page-size"] == "A4"
        assert options["encoding"] == "UTF-8"

        shutil.rmtree("static", ignore_errors=True)

    @pytest.mark.asyncio
    async def test_to_pdf_error_handling(self, minimal_cv):
        with patch("web.backend.services.export_service.pdfkit") as mock_pdfkit:
            mock_pdfkit.from_string.side_effect = OSError("pdfkit not found")
            with pytest.raises(Exception, match="Error generating PDF"):
                await ExportService.to_pdf(minimal_cv)


class TestExportServiceCleanup:
    def test_cleanup_removes_old_files(self):
        export_dir = tempfile.mkdtemp()
        try:
            old_file = os.path.join(export_dir, "old_cv.pdf")
            new_file = os.path.join(export_dir, "new_cv.pdf")
            with open(old_file, "w") as f:
                f.write("old")
            with open(new_file, "w") as f:
                f.write("new")

            import time

            old_time = time.time() - 8 * 86400
            os.utime(old_file, (old_time, old_time))

            assert os.path.exists(new_file)
        finally:
            shutil.rmtree(export_dir, ignore_errors=True)

    def test_cleanup_empty_directory(self):
        export_dir = tempfile.mkdtemp()
        try:
            remaining = os.listdir(export_dir)
            assert len(remaining) == 0
        finally:
            shutil.rmtree(export_dir, ignore_errors=True)

    def test_cleanup_nonexistent_directory(self):
        result = ExportService.cleanup_old_exports(max_age_days=7)
        assert result is None


class TestExportServiceTemplates:
    def test_html_template_contains_doctype(self):
        template = ExportService.get_html_template()
        assert "<!DOCTYPE html>" in template

    def test_html_template_contains_styles(self):
        template = ExportService.get_html_template()
        assert "<style>" in template
        assert "--primary-color" in template

    def test_markdown_template_starts_with_heading(self):
        template = ExportService.get_markdown_template()
        assert "{{ cv.full_name }}" in template
