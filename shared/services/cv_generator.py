import os
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader
import pdfkit
import markdown2
from shared.constants import TEMPLATE_DIR, ALLOWED_EXPORT_FORMATS
from shared.utils.file_handler import FileHandler


class CVGenerationError(Exception):
    pass


class CVGenerator:
    def __init__(self):
        self.template_env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True
        )
        self.file_handler = FileHandler()

    async def generate(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates CV in HTML format from the provided data.
        """
        try:
            template = self.template_env.get_template("cv_template.html")
            html = template.render(data)
            return {"html": html}
        except Exception as e:
            raise CVGenerationError(f"Error generating CV: {str(e)}")

    async def export(self, data: Dict[str, Any], format: str = "pdf") -> Dict[str, Any]:
        """
        Exports CV in the specified format.
        """
        if format not in ALLOWED_EXPORT_FORMATS:
            raise ValueError(f"Unsupported format: {format}")

        try:
            html = (await self.generate(data))["html"]

            if format == "pdf":
                pdf = pdfkit.from_string(html, False)
                return {"pdf": pdf}
            elif format == "html":
                return {"html": html}
            elif format == "md":
                md = markdown2.markdown(html)
                return {"markdown": md}

        except Exception as e:
            raise CVGenerationError(f"Error exporting CV: {str(e)}")

    def get_available_templates(self) -> List[str]:
        """
        Returns a list of available CV templates.
        """
        try:
            templates = []
            for file in os.listdir(TEMPLATE_DIR):
                if file.endswith(".html"):
                    templates.append(file)
            return templates
        except Exception as e:
            raise CVGenerationError(f"Error getting templates: {str(e)}")

    async def _process_photo(
        self, photo_data: Optional[str], filename: str
    ) -> Optional[str]:
        """
        Processes and optimizes photo for CV.
        """
        if not photo_data:
            return None

        try:
            return self.file_handler.save_photo(photo_data, filename)
        except Exception as e:
            raise CVGenerationError(f"Error processing photo: {str(e)}")
