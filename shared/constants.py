from enum import Enum
from typing import Dict

class Language(str, Enum):
    EN = "en"
    ES = "es"

LANGUAGES: Dict[str, Dict[str, Dict[str, str]]] = {
    "en": {
        "labels": {
            "main_title": "Personal Information",
            "name": "Name",
            "title": "Title",
            "age": "Age",
            "city": "City",
            "summary": "Summary",
            "photo": "Photo",
            "phone": "Phone",
            "attach_photo": "Attach Photo",
            "show_photo": "Show Photo",
            "add_professional_experience": "Add Professional Experience",
            "add_academic_experience": "Add Academic Experience",
            "add_skills_experience": "Add Skills",
            "add_certificates_experience": "Add Certificates",
            "generate_cv": "Generate CV",
            "load_json": "Load Data",
            "save_changes": "Save Changes",
            "clear_data": "Clear Data",
            "professional_experience": "Professional Experience",
            "academic_experience": "Academic Experience",
            "skills": "Skills",
            "certificates": "Certificates",
            "company": "Company",
            "position": "Position",
            "start_date": "Start Date",
            "end_date": "End Date",
            "description": "Description",
            "institution": "Institution",
            "degree": "Degree",
            "new_skill": "New Skill",
            "remove": "Remove",
            "date": "Date",
            "export_md": "Export as Markdown",
            "export_pdf": "Export as PDF",
            "gift_coffee": "Gift me a coffee"
        }
    },
    "es": {
        "labels": {
            "main_title": "Información Personal",
            "name": "Nombre",
            "title": "Título",
            "age": "Edad",
            "city": "Ciudad",
            "summary": "Resumen",
            "photo": "Foto",
            "phone": "Teléfono",
            "attach_photo": "Adjuntar Foto",
            "show_photo": "Mostrar Foto",
            "add_professional_experience": "Agregar Experiencia Profesional",
            "add_academic_experience": "Añadir Experiencia Académica",
            "add_skills_experience": "Agregar Habilidades",
            "add_certificates_experience": "Agregar Certificados",
            "generate_cv": "Generar CV",
            "load_json": "Cargar Datos",
            "save_changes": "Guardar Cambios",
            "clear_data": "Limpiar Datos",
            "professional_experience": "Experiencia Profesional",
            "academic_experience": "Experiencia Académica",
            "skills": "Habilidades",
            "certificates": "Certificados",
            "company": "Empresa",
            "position": "Puesto",
            "start_date": "Fecha de inicio",
            "end_date": "Fecha de fin",
            "description": "Descripción",
            "institution": "Institución",
            "degree": "Título",
            "new_skill": "Nueva Habilidad",
            "remove": "Eliminar",
            "date": "Fecha",
            "export_md": "Exportar como Markdown",
            "export_pdf": "Exportar como PDF",
            "gift_coffee": "Regálame un café"
        }
    }
}

# Configuración de la aplicación
APP_NAME = "CV Generator"
DEFAULT_LANGUAGE = Language.EN
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# Configuración de rutas
TEMPLATE_DIR = "shared/templates"
STATIC_DIR = "shared/static"
UPLOAD_DIR = "shared/uploads"

# Configuración de exportación
ALLOWED_EXPORT_FORMATS = ["html", "pdf", "md"]
DEFAULT_EXPORT_FORMAT = "pdf"

# Configuración de la base de datos (si se necesita en el futuro)
DATABASE_URL = "sqlite:///./cv_generator.db" 