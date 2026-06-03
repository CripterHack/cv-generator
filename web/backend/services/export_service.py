from ..models.cv import CV
import pdfkit
from jinja2 import Template
import os
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExportService:
    @staticmethod
    def get_html_template() -> str:
        """
        Retorna la plantilla HTML para la generación del CV.
        """
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ cv.full_name }} - CV</title>
            <style>
                /* Estilos base */
                :root {
                    --primary-color: #2292a7;
                    --text-color: #333;
                    --border-color: #ddd;
                }
                
                body {
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    max-width: 21cm;
                    margin: 0 auto;
                    padding: 2cm;
                    color: var(--text-color);
                }
                
                /* Encabezado y secciones */
                h1, h2, h3 {
                    color: var(--primary-color);
                    margin-bottom: 0.5em;
                }
                
                h1 {
                    border-bottom: 2px solid var(--primary-color);
                    padding-bottom: 0.5cm;
                }
                
                h2 {
                    border-bottom: 1px solid var(--border-color);
                    margin-top: 1cm;
                }
                
                /* Información de contacto */
                .contact-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 0.5cm;
                    margin: 1cm 0;
                }
                
                .contact-item {
                    display: flex;
                    justify-content: space-between;
                    flex-wrap: wrap;
                    align-items: center;
                    gap: 0.5em;
                }
                .contact-info p {
                    margin: 0.2cm 0;
                }

                /* Secciones de experiencia y educación */
                .section {
                    margin: 1cm 0;
                }
                
                .item {
                    margin-bottom: 0.8cm;
                    break-inside: avoid;
                }
                
                .item-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: baseline;
                    margin-bottom: 0.3cm;
                }
                
                .item-title {
                    font-weight: bold;
                    color: var(--primary-color);
                }
                
                .item-period {
                    color: #666;
                    font-size: 0.9em;
                }
                
                /* Habilidades */
                .skills-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                    gap: 0.5cm;
                }
                
                .skill-item {
                    background: #f5f5f5;
                    padding: 0.3cm;
                    border-radius: 4px;
                    display: flex;
                    justify-content: space-between;
                }
                
                /* Ajustes de impresión */
                @media print {
                    body {
                        padding: 0;
                    }
                    
                    .page-break {
                        page-break-before: always;
                    }
                    
                    a {
                        text-decoration: none;
                        color: var(--text-color);
                    }
                }
            </style>
        </head>
        <body>
            <header>
                <h1>{{ cv.full_name }}</h1>
                
                <div class="contact-info">
                    <div class="contact-item">
                        <span>📧</span>
                        <a href="mailto:{{ cv.email }}">{{ cv.email }}</a>
                    </div>
                    {% if cv.phone %}
                    <div class="contact-item">
                        <span>📱</span>
                        <span>{{ cv.phone }}</span>
                    </div>
                    {% endif %}
                    {% if cv.website %}
                    <div class="contact-item">
                        <span>🌐</span>
                        <a href="{{ cv.website }}">{{ cv.website }}</a>
                    </div>
                    {% endif %}
                    {% if cv.linkedin %}
                    <div class="contact-item">
                        <span>💼</span>
                        <a href="{{ cv.linkedin }}">LinkedIn</a>
                    </div>
                    {% endif %}
                    {% if cv.github %}
                    <div class="contact-item">
                        <span>💻</span>
                        <a href="{{ cv.github }}">GitHub</a>
                    </div>
                    {% endif %}
                </div>
            </header>

            {% if cv.summary %}
            <section class="section">
                <h2>Professional Summary</h2>
                <p>{{ cv.summary }}</p>
            </section>
            {% endif %}

            {% if cv.experience %}
            <section class="section">
                <h2>Professional Experience</h2>
                {% for exp in cv.experience %}
                <div class="item">
                    <div class="item-header">
                        <span class="item-title">{{ exp.position }} at {{ exp.company }}</span>
                        <span class="item-period">
                            {{ exp.start_date }} - {{ exp.end_date or 'Present' }}
                            {% if exp.location %} | {{ exp.location }}{% endif %}
                        </span>
                    </div>
                    {% if exp.description %}
                    <p>{{ exp.description }}</p>
                    {% endif %}
                    {% if exp.achievements %}
                    <ul>
                        {% for achievement in exp.achievements %}
                        <li>{{ achievement }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                    {% if exp.technologies %}
                    <p><strong>Technologies:</strong> {{ exp.technologies|join(', ') }}</p>
                    {% endif %}
                </div>
                {% endfor %}
            </section>
            {% endif %}

            {% if cv.education %}
            <section class="section">
                <h2>Education</h2>
                {% for edu in cv.education %}
                <div class="item">
                    <div class="item-header">
                        <span class="item-title">{{ edu.degree }} in {{ edu.field_of_study }}</span>
                        <span class="item-period">{{ edu.start_date }} - {{ edu.end_date or 'Present' }}</span>
                    </div>
                    <p>{{ edu.institution }}</p>
                    {% if edu.description %}
                    <p>{{ edu.description }}</p>
                    {% endif %}
                </div>
                {% endfor %}
            </section>
            {% endif %}

            {% if cv.skills %}
            <section class="section">
                <h2>Skills</h2>
                <div class="skills-grid">
                    {% for skill in cv.skills %}
                    <div class="skill-item">
                        <span>{{ skill.name }}</span>
                        {% if skill.level %}
                        <span>{{ skill.level }}/5</span>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}

            {% if cv.languages %}
            <section class="section">
                <h2>Languages</h2>
                <div class="skills-grid">
                    {% for lang in cv.languages %}
                    <div class="skill-item">
                        <span>{{ lang.name }}</span>
                        <span>{{ lang.level }}</span>
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endif %}

            {% if cv.certificates %}
            <section class="section">
                <h2>Certificates</h2>
                <ul>
                    {% for cert in cv.certificates %}
                    <li>
                        {{ cert.name }} - {{ cert.issuer }} ({{ cert.date_obtained }})
                        {% if cert.credential_url %}
                        <a href="{{ cert.credential_url }}">[View Certificate]</a>
                        {% endif %}
                    </li>
                    {% endfor %}
                </ul>
            </section>
            {% endif %}
        </body>
        </html>
        """

    @staticmethod
    def get_markdown_template() -> str:
        return """
        # {{ cv.full_name }}

        {% if cv.phone or cv.email or cv.website %}
        ## Contact Information
        {% if cv.email %}* Email: {{ cv.email }}{% endif %}
        {% if cv.phone %}* Phone: {{ cv.phone }}{% endif %}
        {% if cv.website %}* Website: {{ cv.website }}{% endif %}
        {% if cv.linkedin %}* LinkedIn: {{ cv.linkedin }}{% endif %}
        {% if cv.github %}* GitHub: {{ cv.github }}{% endif %}
        {% endif %}

        {% if cv.summary %}
        ## Professional Summary
        {{ cv.summary }}
        {% endif %}

        {% if cv.experience %}
        ## Professional Experience
        {% for exp in cv.experience %}
        ### {{ exp.position }} at {{ exp.company }}
        *{{ exp.start_date }} - {{ exp.end_date or 'Present' }}*{% if exp.location %} | {{ exp.location }}{% endif %}

        {% if exp.description %}{{ exp.description }}{% endif %}

        {% if exp.achievements %}
        **Key Achievements:**
        {% for achievement in exp.achievements %}
        * {{ achievement }}
        {% endfor %}
        {% endif %}

        {% if exp.technologies %}
        **Technologies:** {{ exp.technologies|join(', ') }}
        {% endif %}

        {% endfor %}
        {% endif %}

        {% if cv.education %}
        ## Education
        {% for edu in cv.education %}
        ### {{ edu.degree }} in {{ edu.field_of_study }}
        *{{ edu.institution }}* | {{ edu.start_date }} - {{ edu.end_date or 'Present' }}

        {% if edu.description %}{{ edu.description }}{% endif %}

        {% endfor %}
        {% endif %}

        {% if cv.skills %}
        ## Skills
        {% for skill in cv.skills %}
        * {{ skill.name }}{% if skill.level %} (Level: {{ skill.level }}/5){% endif %}{% if skill.category %} - {{ skill.category }}{% endif %}
        {% endfor %}
        {% endif %}

        {% if cv.languages %}
        ## Languages
        {% for lang in cv.languages %}
        * {{ lang.name }} - {{ lang.level }}{% if lang.certification %} ({{ lang.certification }}){% endif %}
        {% endfor %}
        {% endif %}

        {% if cv.certificates %}
        ## Certificates
        {% for cert in cv.certificates %}
        * {{ cert.name }} - {{ cert.issuer }} ({{ cert.date_obtained }}){% if cert.credential_url %}
          [View Certificate]({{ cert.credential_url }}){% endif %}
        {% endfor %}
        {% endif %}
        """

    @staticmethod
    async def to_pdf(cv: CV) -> str:
        """
        Convierte el CV a formato PDF usando una plantilla HTML.
        """
        try:
            # Asegurarse de que el directorio de exportación existe
            export_dir = "static/exports"
            os.makedirs(export_dir, exist_ok=True)

            # Generar el contenido HTML
            template = Template(ExportService.get_html_template())
            html_content = template.render(cv=cv)

            # Configurar opciones de PDF
            options = {
                "page-size": "A4",
                "margin-top": "0.75in",
                "margin-right": "0.75in",
                "margin-bottom": "0.75in",
                "margin-left": "0.75in",
                "encoding": "UTF-8",
                "no-outline": None,
                "enable-local-file-access": None,
                "print-media-type": None,
                "javascript-delay": "1000",
                "no-stop-slow-scripts": None,
            }

            # Generar nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(export_dir, f"cv_{cv.email}_{timestamp}.pdf")

            # Generar PDF
            logger.info(f"Generando PDF en: {output_path}")
            pdfkit.from_string(html_content, output_path, options=options)
            logger.info("PDF generado exitosamente")

            return output_path
        except Exception as e:
            logger.error(f"Error generando PDF: {str(e)}")
            raise Exception(f"Error generating PDF: {str(e)}")

    @staticmethod
    async def to_markdown(cv: CV) -> str:
        """
        Convierte el CV a formato Markdown.
        """
        try:
            template = Template(ExportService.get_markdown_template())
            return template.render(cv=cv)
        except Exception as e:
            logger.error(f"Error generando Markdown: {str(e)}")
            raise Exception(f"Error generating Markdown: {str(e)}")

    @staticmethod
    async def to_html(cv: CV) -> str:
        """
        Convierte el CV a formato HTML.
        """
        try:
            template = Template(ExportService.get_html_template())
            return template.render(cv=cv)
        except Exception as e:
            logger.error(f"Error generando HTML: {str(e)}")
            raise Exception(f"Error generating HTML: {str(e)}")

    @staticmethod
    def cleanup_old_exports(max_age_days: int = 7):
        """
        Limpia archivos de exportación antiguos.
        """
        try:
            export_dir = "static/exports"
            if not os.path.exists(export_dir):
                return

            current_time = datetime.now()
            for filename in os.listdir(export_dir):
                filepath = os.path.join(export_dir, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if (current_time - file_modified).days > max_age_days:
                    os.remove(filepath)
                    logger.info(f"Archivo antiguo eliminado: {filepath}")
        except Exception as e:
            logger.error(f"Error limpiando archivos antiguos: {str(e)}")
