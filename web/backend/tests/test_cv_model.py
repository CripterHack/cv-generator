import pytest
from pydantic import ValidationError
from web.backend.models.cv import (
    CV,
    Education,
    Experience,
    Skill,
    Certificate,
    Language,
)


class TestCVModel:
    def test_minimal_valid_cv(self):
        cv = CV(full_name="Jane Doe", email="jane@example.com")
        assert cv.full_name == "Jane Doe"
        assert cv.email == "jane@example.com"
        assert cv.experience == []
        assert cv.education == []
        assert cv.skills == []
        assert cv.certificates == []
        assert cv.languages == []
        assert cv.version == 1

    def test_missing_full_name_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            CV(email="jane@example.com")
        assert "full_name" in str(exc_info.value)

    def test_missing_email_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            CV(full_name="Jane Doe")
        assert "email" in str(exc_info.value)

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            CV(full_name="Jane Doe", email="not-an-email")
        assert "email" in str(exc_info.value)

    def test_model_dump_roundtrip(self):
        cv = CV(
            full_name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            summary="A developer",
        )
        data = cv.model_dump()
        restored = CV(**data)
        assert restored.full_name == cv.full_name
        assert restored.email == cv.email
        assert restored.phone == cv.phone
        assert restored.summary == cv.summary

    def test_default_version_is_one(self):
        cv = CV(full_name="Test", email="test@example.com")
        assert cv.version == 1

    def test_optional_fields_default_none(self):
        cv = CV(full_name="Test", email="test@example.com")
        assert cv.phone is None
        assert cv.summary is None
        assert cv.website is None
        assert cv.linkedin is None
        assert cv.github is None
        assert cv.photo_url is None
        assert cv.created_at is None
        assert cv.updated_at is None


class TestExperienceModel:
    def test_valid_experience(self):
        exp = Experience(
            company="Tech Corp",
            position="Developer",
            start_date="2020-01-01",
        )
        assert exp.company == "Tech Corp"
        assert exp.end_date is None
        assert exp.achievements is None
        assert exp.technologies is None

    def test_full_experience(self):
        exp = Experience(
            company="Tech Corp",
            position="Developer",
            start_date="2020-01-01",
            end_date="2023-12-31",
            description="Built things",
            location="Remote",
            achievements=["Shipped v1", "Led team"],
            technologies=["Python", "Docker"],
        )
        assert exp.location == "Remote"
        assert len(exp.achievements) == 2
        assert len(exp.technologies) == 2

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            Experience(company="Tech Corp", start_date="2020-01-01")


class TestEducationModel:
    def test_valid_education(self):
        edu = Education(
            institution="MIT",
            degree="BSc",
            field_of_study="CS",
            start_date="2018-01-01",
        )
        assert edu.end_date is None
        assert edu.achievements is None

    def test_missing_institution_raises(self):
        with pytest.raises(ValidationError):
            Education(degree="BSc", field_of_study="CS", start_date="2018-01-01")


class TestSkillModel:
    def test_valid_skill(self):
        skill = Skill(name="Python")
        assert skill.level is None
        assert skill.category is None

    def test_skill_with_level(self):
        skill = Skill(name="Python", level=5)
        assert skill.level == 5

    def test_skill_level_too_low_raises(self):
        with pytest.raises(ValidationError):
            Skill(name="Python", level=0)

    def test_skill_level_too_high_raises(self):
        with pytest.raises(ValidationError):
            Skill(name="Python", level=6)

    def test_skill_level_boundary_valid(self):
        Skill(name="A", level=1)
        Skill(name="B", level=5)

    def test_missing_name_raises(self):
        with pytest.raises(ValidationError):
            Skill()


class TestCertificateModel:
    def test_valid_certificate(self):
        cert = Certificate(
            name="AWS SA",
            issuer="Amazon",
            date_obtained="2023-01-01",
        )
        assert cert.credential_url is None
        assert cert.credential_id is None
        assert cert.expiry_date is None

    def test_full_certificate(self):
        cert = Certificate(
            name="AWS SA",
            issuer="Amazon",
            date_obtained="2023-01-01",
            expiry_date="2025-01-01",
            credential_id="ABC-123",
            credential_url="https://aws.amazon.com/cert/123",
        )
        assert cert.credential_id == "ABC-123"


class TestLanguageModel:
    def test_valid_language(self):
        lang = Language(name="English", level="Native")
        assert lang.certification is None

    def test_missing_level_raises(self):
        with pytest.raises(ValidationError):
            Language(name="English")


class TestCVWithNestedModels:
    def test_full_cv_with_all_fields(self):
        cv = CV(
            full_name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            summary="Engineer",
            experience=[
                Experience(
                    company="Corp",
                    position="Dev",
                    start_date="2020-01-01",
                    technologies=["Python"],
                ),
            ],
            education=[
                Education(
                    institution="MIT",
                    degree="BSc",
                    field_of_study="CS",
                    start_date="2016-01-01",
                    end_date="2020-01-01",
                ),
            ],
            skills=[Skill(name="Python", level=5)],
            certificates=[
                Certificate(name="AWS", issuer="Amazon", date_obtained="2022-01-01"),
            ],
            languages=[Language(name="English", level="Native")],
            website="https://example.com",
            linkedin="https://linkedin.com/in/test",
            github="https://github.com/test",
        )
        assert len(cv.experience) == 1
        assert len(cv.education) == 1
        assert len(cv.skills) == 1
        assert len(cv.certificates) == 1
        assert len(cv.languages) == 1

    def test_model_dump_includes_nested(self):
        cv = CV(
            full_name="John Doe",
            email="john@example.com",
            skills=[Skill(name="Python", level=5), Skill(name="Go", level=3)],
        )
        data = cv.model_dump()
        assert len(data["skills"]) == 2
        assert data["skills"][0]["name"] == "Python"

    def test_empty_collections_are_valid(self):
        cv = CV(
            full_name="Test",
            email="test@example.com",
            experience=[],
            education=[],
            skills=[],
        )
        assert cv.experience == []
