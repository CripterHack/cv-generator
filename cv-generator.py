import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import base64
from jinja2 import Template
import webbrowser
import os
import time
import json
from PIL import Image, ImageTk
from io import BytesIO
import logging
logging.basicConfig(level=logging.DEBUG)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import markdown2
import pdfkit

class Curriculum:
    def __init__(self):
        """Initializes the Curriculum class and sets up the GUI."""
        self.is_data_modified = False
        self.root = tk.Tk()
        self.root.title("Curriculum Generator")
        self.root.geometry("900x750")
        self.languages = self.get_languages()
        self.current_language = "en"
        self.data_file = "curriculum_data.json"
        self.foto_encoded = ""
        self.mostrar_foto = tk.BooleanVar(value=False)
        self.professional_experience = []
        self.academic_experience = []
        self.skills = []
        self.certificates = []

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(script_dir, "curriculum_data.json")
    
        self.setup_gui()
        self.setup_favicon()
        self.load_default_data()

    def setup_gui(self):
        """Sets up the entire user interface."""
        # Left and right frames for UI and preview respectively
        left_frame = self.create_frame(self.root, 0, 0)
        self.preview_frame = self.create_frame(self.root, 0, 1)

        # Language Toggle Button
        self.language_button = self.create_button(left_frame, self.languages[self.current_language]["language_toggle"], self.toggle_language, 0)

        # Personal Information
        fields = ["name", "title", "phone", "age", "city", "summary"]
        for index, field in enumerate(fields, 1):
            self.create_entry(left_frame, field, index)

        self.name_label = tk.Label(left_frame, text=self.languages[self.current_language]["name"])
        self.title_label = tk.Label(left_frame, text=self.languages[self.current_language]["title"])
        self.phone_label = tk.Label(left_frame, text=self.languages[self.current_language]["phone"])
        self.age_label = tk.Label(left_frame, text=self.languages[self.current_language]["age"])
        self.city_label = tk.Label(left_frame, text=self.languages[self.current_language]["city"])
        self.summary_label = tk.Label(left_frame, text=self.languages[self.current_language]["summary"])

        # Other UI elements
        self.photo_button = self.create_button(left_frame, self.languages[self.current_language]["attach_photo"], self.attach_photo, 7)
        self.checkbox_photo = tk.Checkbutton(left_frame, text=self.languages[self.current_language]["show_photo"], variable=self.mostrar_foto, command=self.update_preview)
        self.checkbox_photo.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # Add Experience, Skills, Certificates
        self.create_section_buttons(left_frame)

        # Load, Save, Clear, and Generate Buttons
        self.create_main_buttons(left_frame)

        # Preview Text Area
        self.setup_preview_area()

        # Footer for GitHub link
        self.create_footer()

    def setup_favicon(self):
        """Sets up the application favicon."""
        icon_data = b"iVBORw0KGgoAAAANSUhEUgAAAMAAAADABAMAAACg8nE0AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAJcEhZcwAAGJsAABibAUl1g5QAAAAhUExURQAAAP///wUFBfz8/C4uLuHh4ZmZmU5OTsbGxoqKinBwcEeuAmIAAANbSURBVHja7Zyxb9NAFMZPpygEttORNs10iqgE4wlXrKnaqZsDE1NhAEY6sSZISFGngljYmpW/kvjuObEd2zJ37zUEvaeqUqzqfv6+s++9d44rBAcHx38TcoIe5mEVvPiAHj9KgFOtkMPOKoCXyLEDIFdAD0A1ye5DwfgLYqxqAE8x76vzOgDicmHO96KAAQxgAAMYwAAGMIABDGCAj7/q6jsBoF+gU3B6tu7mXr/Jcb9a4mMYwDVz+eFnLQ2fPpJBgKzztAl86rW1uYGAkoIegQIGBAF29iQcYEyswM4R7oOeO1l7+7sU79zR4RQBYNxYlXOVi+ygPpYIAHGh/FjFRe6x2wWy1wYBIPvZYHpU/Atz46BDIzAU+ElQ0x2H1CuJAjDfbcUOCQ7d4SiAz0nBIT8to+B8UAb489UnsupQggQQMnXXvKk6dG+QAGZlS+OBQ0cSSwFkoFnZocpAURY90cXbNnfos0FTIFNbvGi8QycSTUE+CXDK4NBXgQcQz/V2vfOGKT01eAD5SBeOXNSnmigFInMlvy4XtjbVRAHMjVv+p1uHdlNNnIKB3ixueXpABcAkzLYOXRtcBX4S1hMLN93QCFyAmwQ3rHNINTkUrsBPwnq98w7dYSvw1ZGdg0MjI7ABMite9DE4lAh0gBt5vd4tbFOqiQPIiSte1JX2qSbv/wyeAle82G+qMdVEAC5d+ETvAD8vN4ECSH35u/mlLGp/kAPIGhCfMBmwZwA0fn5M9E7/ARR8Wvpwh4fLYryVaEsF5LK2ZSIS4Gvq+ooUBVCqjQgAUA/NBJlFnRyKUeAdElQKoOtIyABwDd0bMgUL29AZIyX9jg5FlI6qtaCLV5DatpI3vnzv67amAKvDaWwKEBS4lNDBodAus7NDoY04OCTIFKSbJpMEAA6NJRUAHJoLMgWp6upQWFXR183bNyjbmivboZyI2ZhNOyXLcMBAqw7lRMTuu3NIdXMo4vlBN4dCAOCQoFIADp0ta+M2vvjtWeKnUANd03cgNiDgEJ0C/3SCAVWAm9HkgBX4b/S/L+7lNEbQnQx5ZpMPZPNP2FIhi1+ZkBP871XEBAMYwAAGMIABDGAAAxjwTwMO/qVD8hc/+eXbvb+ffOivcJO/Rk8eh/+vDDg4OCjjDyLt+3UpQer+AAAAV3pUWHRSYXcgcHJvZmlsZSB0eXBlIGlwdGMAAHic4/IMCHFWKCjKT8vMSeVSAAMjCy5jCxMjE0uTFAMTIESANMNkAyOzVCDL2NTIxMzEHMQHy4BIoEouAOoXEXTyQjWVAAAAAElFTkSuQmCC"
        image = Image.open(BytesIO(base64.b64decode(icon_data)))
        photo = ImageTk.PhotoImage(image)
        self.root.iconphoto(False, photo)

    def load_default_data(self):
        """Loads default data from the JSON file."""
        logging.debug(f"Attempting to load data from {self.data_file}")
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.update_fields_from_json(data)
        except FileNotFoundError:
            # If the file does not exist, simply initialize with empty values
            messagebox.showwarning("File Not Found", f"Could not find the data file at {self.data_file}.")
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Error", "The file is corrupted or empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        self.update_preview()

    def create_frame(self, parent, row, col):
        """Creates a Tkinter frame with basic configuration."""
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.grid(row=row, column=col, sticky="nsew")
        self.root.grid_columnconfigure(col, weight=2 if col == 1 else 1)
        self.root.grid_rowconfigure(row, weight=1)
        return frame

    def create_entry(self, parent, field, row):
        """Creates a labeled entry field with real-time preview binding."""
        label = tk.Label(parent, text=self.languages[self.current_language][field])
        label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        entry.bind("<KeyRelease>", lambda e: self.set_data_modified(True))
        setattr(self, field, entry)

    def create_button(self, parent, text, command, row):
        """Creates a Tkinter button."""
        button = tk.Button(parent, text=text, command=command)
        button.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        return button

    def create_section_buttons(self, parent):
        """Creates buttons for adding experiences, skills, and certificates."""
        self.professional_experience_button = self.create_button(parent, self.languages[self.current_language]["add_professional_experience"], self.add_professional_experience, 9)
        self.academic_experience_button = self.create_button(parent, self.languages[self.current_language]["add_academic_experience"], self.add_academic_experience, 10)
        self.skills_button = self.create_button(parent, self.languages[self.current_language]["add_skills_experience"], self.add_skill, 11)
        self.certificates_button = self.create_button(parent, self.languages[self.current_language]["add_certificates_experience"], self.add_certificate, 12)

    def add_certificate(self):
        """Adds a new certificate."""
        self.add_entry_to_list("certificates", "name", "institution", "date")

    def remove_experience(self, section, index):
        """Removes an experience entry from a given section."""
        if index < len(getattr(self, section)):
            del getattr(self, section)[index]
            self.set_data_modified(True)
            self.update_preview()

    def create_main_buttons(self, parent):
        """Creates Load, Save, Clear, and Generate buttons."""
        button_frame = tk.Frame(parent)
        button_frame.grid(row=13, column=0, columnspan=2, pady=10)

        self.load_button = tk.Button(button_frame, text=self.languages[self.current_language]["load_json"], command=self.load_json_file)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text=self.languages[self.current_language]["save_changes"], command=self.save_data_from_preview)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text=self.languages[self.current_language]["clear_data"], command=self.clear_data)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.generate_button = tk.Button(button_frame, text=self.languages[self.current_language]["generate_cv"], command=self.generate_curriculum)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.export_md_button = tk.Button(button_frame, text=self.languages[self.current_language]["export_md"], command=self.export_as_markdown)
        self.export_md_button.pack(side=tk.LEFT, padx=5)

        self.export_pdf_button = tk.Button(button_frame, text=self.languages[self.current_language]["export_pdf"], command=self.export_as_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=5)

    def setup_preview_area(self):
        """Sets up the preview area with a canvas and a scrollbar."""
        self.preview_canvas = tk.Canvas(self.preview_frame)
        self.preview_scrollbar = tk.Scrollbar(self.preview_frame, orient="vertical", command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)

        self.preview_scrollbar.pack(side="right", fill="y")
        self.preview_canvas.pack(side="left", fill="both", expand=True)

        self.preview_content = tk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_content, anchor='nw')

        self.preview_content.bind("<Configure>", lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all")))

    def create_footer(self):
        """Adds a footer with GitHub link at the bottom of the main window."""
        footer = tk.Label(self.root, text="GitHub @cripterhack", fg="blue", cursor="hand2")
        footer.grid(row=2, column=0, columnspan=2, pady=5)
        footer.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/CripterHack"))

    def get_languages(self):
        """Returns a dictionary of languages."""
        return {
            "en": {
                "main_title": "Personal Information", "name": "Name", "title": "Title", "age": "Age", "city": "City", "summary": "Summary",
                "photo": "Photo", "phone": "Phone / Whatsapp", "attach_photo": "Attach Photo", "show_photo": "Show Photo", "add_professional_experience": "Add Professional Experience", "add_academic_experience": "Add Academic Experience", "add_skills_experience": "Add Skills Experience", "add_certificates_experience": "Add Certificates Experience",
                "generate_cv": "Generate CV", "load_json": "Load Data", "save_changes": "Save Changes", "clear_data": "Clear Data",
                "professional_experience": "Professional Experience", "academic_experience": "Academic Experience",
                "skills": "Skills", "certificates": "Certificates", "language_toggle": "Cambiar a Español",
                "company": "Company", "position": "Position", "start_date": "Start Date", "end_date": "End Date", "description": "Description",
                "institution": "Institution", "degree": "Degree", "new_skill": "New Skill", "remove": "Remove", "date": "Date", "export_md": "Export as Markdown", "export_pdf": "Export as PDF"
            },
            "es": {
                "main_title": "Información Personal", "name": "Nombre", "title": "Título", "age": "Edad", "city": "Ciudad", "summary": "Resumen",
                "photo": "Foto", "phone": "Teléfono / Whatsapp", "attach_photo": "Adjuntar Foto", "show_photo": "Mostrar Foto", "add_professional_experience": "Agregar Experiencia Profesional", "add_academic_experience": "Añadir Experiencia Académica", "add_skills_experience": "Agregar Habilidades", "add_certificates_experience": "Agregar Certificados",
                "generate_cv": "Generar CV", "load_json": "Cargar Datos", "save_changes": "Guardar Cambios", "clear_data": "Limpiar Datos",
                "professional_experience": "Experiencia Profesional", "academic_experience": "Experiencia Académica",
                "skills": "Habilidades", "certificates": "Certificados", "language_toggle": "Switch to English",
                "company": "Empresa", "position": "Puesto", "start_date": "Fecha de inicio", "end_date": "Fecha de fin", "description": "Descripción",
                "institution": "Institución", "degree": "Título", "new_skill": "Nueva Habilidad", "remove": "Eliminar", "date": "Fecha", "export_md": "Exportar como Markdown", "export_pdf": "Exportar como PDF"
            }
        }
    
    def export_as_markdown(self):
        """Exports the curriculum as a Markdown file."""
        markdown_content = self.render_markdown()
        timestamp_hex = hex(int(time.time()))[2:].upper()
        filename = f"curriculum-{self.current_language}-{timestamp_hex}.md"
        try:
            with open(filename, "w", encoding='utf-8') as f:
                f.write(markdown_content)
            messagebox.showinfo("Éxito", f"CV exportado como Markdown: {filename}")
        except Exception as e:
            messagebox.showerror("Error de exportación", f"Ocurrió un error al exportar el CV como Markdown: {str(e)}")

    def export_as_pdf(self):
        """Exports the curriculum as a PDF file."""
        html_content = self.render_html()
        timestamp_hex = hex(int(time.time()))[2:].upper()
        filename = f"curriculum-{self.current_language}-{timestamp_hex}.pdf"
        try:
            pdfkit.from_string(html_content, filename)
            messagebox.showinfo("Éxito", f"CV exportado como PDF: {filename}")
        except Exception as e:
            messagebox.showerror("Error de exportación", f"Ocurrió un error al exportar el CV como PDF: {str(e)}")

    def render_experience_markdown(self, experiences, is_academic=False):
        """Renders a list of experiences as Markdown."""
        md = ""
        for exp in experiences:
            if is_academic:
                md += f"- **{exp['institution']}** ({exp['start_date']} - {exp['end_date']}): {exp['degree']}\n"
            else:
                md += f"- **{exp['company']}** ({exp['start_date']} - {exp['end_date']}): {exp['position']}\n"
                if 'description' in exp:
                    md += f"  {exp['description']}\n"
        return md

    def render_markdown(self):
        """Renders the curriculum as a Markdown string."""
        labels = self.languages[self.current_language]
        md = f"""
        # {self.name}

        {self.title.get()}

        {labels['phone']}: {self.phone.get()} | {labels['age']}: {self.age.get()} | {labels['city']}: {self.city.get()}

        ## {labels['summary']}

        {self.summary}

        ## {labels['professional_experience']}

        {self.render_experience_markdown(self.professional_experience)}

        ## {labels['academic_experience']}

        {self.render_experience_markdown(self.academic_experience, is_academic=True)}

        ## {labels['skills']}

        {self.render_list_markdown(self.skills)}

        ## {labels['certificates']}

        {self.render_list_markdown(self.certificates)}
        """
        return md.strip()

    def render_list_markdown(self, items):
        """Renders a list of items as Markdown."""
        return "\n".join([f"- {item}" for item in items])

    def toggle_language(self):
        """Toggles between English and Spanish."""
        self.current_language = "es" if self.current_language == "en" else "en"
        self.update_gui_text()

    def update_gui_text(self):
        """Updates all text in the GUI to match the selected language."""
        self.language_button.config(text=self.languages[self.current_language]["language_toggle"])
        self.name_label.config(text=self.languages[self.current_language]["name"])
        self.title_label.config(text=self.languages[self.current_language]["title"])
        self.phone_label.config(text=self.languages[self.current_language]["phone"])
        self.age_label.config(text=self.languages[self.current_language]["age"])
        self.city_label.config(text=self.languages[self.current_language]["city"])
        self.summary_label.config(text=self.languages[self.current_language]["summary"])
        self.photo_button.config(text=self.languages[self.current_language]["attach_photo"])
        self.checkbox_photo.config(text=self.languages[self.current_language]["show_photo"])

        # Update section buttons
        self.professional_experience_button.config(text=self.languages[self.current_language]["add_professional_experience"])
        self.academic_experience_button.config(text=self.languages[self.current_language]["add_academic_experience"])
        self.skills_button.config(text=self.languages[self.current_language]["add_skills_experience"])
        self.certificates_button.config(text=self.languages[self.current_language]["add_certificates_experience"])

        # Update main operation buttons
        self.load_button.config(text=self.languages[self.current_language]["load_json"])
        self.save_button.config(text=self.languages[self.current_language]["save_changes"])
        self.generate_button.config(text=self.languages[self.current_language]["generate_cv"])
        self.clear_button.config(text=self.languages[self.current_language]["clear_data"])

        # Refresh the preview to reflect language changes
        self.update_preview()

    def attach_photo(self):
        """Allows user to attach a photo."""
        photo = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if photo:
            with open(photo, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                self.foto_encoded = f"data:image/png;base64,{encoded_string}"
            self.set_data_modified(True)

    def add_professional_experience(self):
        """Adds a professional experience entry."""
        self.add_entry_to_list("professional_experience", "company", "position", "start_date", "end_date", "description")

    def add_academic_experience(self):
        """Adds an academic experience entry."""
        self.add_entry_to_list("academic_experience", "institution", "degree", "start_date", "end_date")

    def add_skill(self):
        """Agrega una nueva habilidad."""
        new_skill = simpledialog.askstring(self.languages[self.current_language]["new_skill"], self.languages[self.current_language]["new_skill"] + ":")
        if new_skill:
            self.skills.append(new_skill)
            self.set_data_modified(True)

    def create_skill_entry(self, parent, skill, index):
        """Creates a skill entry in the preview."""
        frame = tk.Frame(parent)
        frame.pack(anchor='w', pady=2)
        entry = tk.Entry(frame)
        entry.pack(side='left', fill='x', expand=True)
        entry.insert(0, skill)
        entry.bind("<FocusOut>", lambda e: self.on_skill_change(index, entry.get()))
        tk.Button(frame, text=self.languages[self.current_language]["remove"], command=lambda: self.remove_skill(index)).pack(side='left', padx=5)

    def on_skill_change(self, index, value):
        """Handles changes to skill entries."""
        if self.skills[index] != value:
            self.skills[index] = value
            self.set_data_modified(True)

    def add_skill_from_entry(self):
        """Adds a new skill from the entry field."""
        new_skill = self.new_skill_entry.get()
        if new_skill:
            self.skills.append(new_skill)
            self.new_skill_entry.delete(0, tk.END)
            self.set_data_modified(True)
            self.update_preview()

    def remove_skill(self, index):
        """Removes a skill entry."""
        if index < len(self.skills):
            del self.skills[index]
            self.set_data_modified(True)
            self.update_preview()

    def add_certificates_section(self):
        """Adds the Certificates section to the preview."""
        tk.Label(self.preview_content, text=self.languages[self.current_language]["certificates"], font=('Arial', 16, 'bold')).pack(anchor='w', pady=(10, 0))
        for index, cert in enumerate(self.certificates):
            self.create_certificate_entry(self.preview_content, cert, index)
        # Entry to add new certificate
        tk.Button(self.preview_content, text=self.languages[self.current_language]["add_certificates_experience"], command=self.add_certificate).pack(anchor='w', pady=5)

    def create_academic_experience_entry(self, parent, exp, index):
        """Creates an academic experience entry in the preview."""
        frame = tk.Frame(parent, bd=1, relief='solid', padx=5, pady=5)
        frame.pack(fill='x', pady=5)
        self.create_labeled_entry(frame, self.languages[self.current_language]["institution"], exp['institution'], lambda val: self.on_experience_change('academic_experience', index, 'institution', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["degree"], exp['degree'], lambda val: self.on_experience_change('academic_experience', index, 'degree', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["start_date"], exp['start_date'], lambda val: self.on_experience_change('academic_experience', index, 'start_date', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["end_date"], exp['end_date'], lambda val: self.on_experience_change('academic_experience', index, 'end_date', val))
        tk.Button(frame, text=self.languages[self.current_language]["remove"], command=lambda: self.remove_experience('academic_experience', index)).pack(anchor='e')

    def create_certificate_entry(self, parent, cert, index):
        """Creates a certificate entry in the preview."""
        frame = tk.Frame(parent, bd=1, relief='solid', padx=5, pady=5)
        frame.pack(fill='x', pady=5)
        self.create_labeled_entry(frame, self.languages[self.current_language]["name"], cert['name'], lambda val: self.on_experience_change('certificates', index, 'name', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["institution"], cert['institution'], lambda val: self.on_experience_change('certificates', index, 'institution', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["date"], cert['date'], lambda val: self.on_experience_change('certificates', index, 'date', val))
        tk.Button(frame, text=self.languages[self.current_language]["remove"], command=lambda: self.remove_experience('certificates', index)).pack(anchor='e')

    def on_experience_change(self, section, index, field, value):
        """Handles changes to experience entries."""
        current_value = getattr(self, section)[index].get(field, None)
        if current_value != value:
            getattr(self, section)[index][field] = value
            self.set_data_modified(True)

    def add_entry_to_list(self, list_name, *fields):
        """Adds a new entry to a specified list."""
        def save_entry():
            entry_data = {field: entries[field].get() for field in fields}
            getattr(self, list_name).append(entry_data)
            self.set_data_modified(True)
            window.destroy()
            self.update_preview()

        window = tk.Toplevel(self.root)
        window.title(f"{self.languages[self.current_language][list_name]}")
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(window, text=self.languages[self.current_language][field]).grid(row=i, column=0, padx=10, pady=5)
            entries[field] = tk.Entry(window)
            entries[field].grid(row=i, column=1, padx=10, pady=5)
        tk.Button(window, text=self.languages[self.current_language]["save_changes"], command=save_entry).grid(row=len(fields), column=1, padx=10, pady=10)

    def load_json_file(self):
        """Loads data from a selected JSON file."""
        file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.data_file = file_path
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.update_fields_from_json(data)
                    messagebox.showinfo("Success", "Data loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        else:
            messagebox.showinfo("No File Selected", "No file was selected.")

    def update_fields_from_json(self, data):
        """Updates fields from JSON data."""
        for field in ["name", "title", "phone", "age", "city", "summary"]:
            getattr(self, field).delete(0, tk.END)
            getattr(self, field).insert(0, data.get(field, ""))
        self.foto_encoded = data.get("foto_encoded", "")
        self.mostrar_foto.set(data.get("mostrar_foto", False))
        self.professional_experience = data.get("professional_experience", [])
        self.academic_experience = data.get("academic_experience", [])
        self.skills = data.get("skills", [])
        self.certificates = data.get("certificates", [])
        self.update_preview()

    def clear_data(self):
        """Clears all data fields."""
        for field in ["name", "title", "phone", "age", "city", "summary"]:
            getattr(self, field).delete(0, tk.END)
        self.foto_encoded = ""
        self.mostrar_foto.set(False)
        self.professional_experience = []
        self.academic_experience = []
        self.skills = []
        self.certificates = []
        self.set_data_modified(True)
        self.update_preview()

    def update_preview(self):
        """Updates the preview area."""
        for widget in self.preview_content.winfo_children():
            widget.destroy()
        self.add_personal_information_section()
        self.add_professional_experience_section()
        self.add_academic_experience_section()
        self.add_skills_section()
        self.add_certificates_section()
        self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))

    def add_personal_information_section(self):
        """Adds the Personal Information section to the preview."""
        tk.Label(self.preview_content, text=self.languages[self.current_language]["main_title"], font=('Arial', 16, 'bold')).pack(anchor='w')
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["name"], self.name.get(), self.name)
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["title"], self.title.get(), self.title)
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["phone"], self.phone.get(), self.phone)
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["age"], self.age.get(), self.age)
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["city"], self.city.get(), self.city)
        self.create_editable_field(self.preview_content, self.languages[self.current_language]["summary"], self.summary.get(), self.summary)

    def add_professional_experience_section(self):
        """Adds the Professional Experience section to the preview."""
        tk.Label(self.preview_content, text=self.languages[self.current_language]["professional_experience"], font=('Arial', 16, 'bold')).pack(anchor='w', pady=(10, 0))
        for index, exp in enumerate(self.professional_experience):
            self.create_professional_experience_entry(self.preview_content, exp, index)
        tk.Button(self.preview_content, text=self.languages[self.current_language]["add_professional_experience"], command=self.add_professional_experience).pack(anchor='w', pady=5)

    def add_academic_experience_section(self):
        """Adds the Academic Experience section to the preview."""
        tk.Label(self.preview_content, text=self.languages[self.current_language]["academic_experience"], font=('Arial', 16, 'bold')).pack(anchor='w', pady=(10, 0))
        for index, exp in enumerate(self.academic_experience):
            self.create_academic_experience_entry(self.preview_content, exp, index)
        tk.Button(self.preview_content, text=self.languages[self.current_language]["add_academic_experience"], command=self.add_academic_experience).pack(anchor='w', pady=5)

    def add_skills_section(self):
        """Adds the Skills section to the preview."""
        tk.Label(self.preview_content, text=self.languages[self.current_language]["skills"], font=('Arial', 16, 'bold')).pack(anchor='w', pady=(10, 0))
        for index, skill in enumerate(self.skills):
            self.create_skill_entry(self.preview_content, skill, index)
        # Add an entry to input new skills
        self.new_skill_entry = tk.Entry(self.preview_content)
        self.new_skill_entry.pack(anchor='w', fill='x', pady=5)
        tk.Button(self.preview_content, text=self.languages[self.current_language]["add_skills_experience"], command=self.add_skill_from_entry).pack(anchor='w', pady=5)

    def create_editable_field(self, parent, label_text, value, variable):
        """Creates an editable field in the preview."""
        frame = tk.Frame(parent)
        frame.pack(anchor='w', pady=2)
        tk.Label(frame, text=label_text + ":", width=15, anchor='w').pack(side='left')
        entry = tk.Entry(frame)
        entry.pack(side='left', fill='x', expand=True)
        entry.insert(0, value)
        entry.bind("<FocusOut>", lambda e: self.on_personal_info_change(variable, entry.get()))

    def on_personal_info_change(self, variable, value):
        """Handles changes to personal information fields."""
        if variable.get() != value:
            variable.delete(0, tk.END)
            variable.insert(0, value)
            self.set_data_modified(True)

    def create_professional_experience_entry(self, parent, exp, index):
        """Creates a professional experience entry in the preview."""
        frame = tk.Frame(parent, bd=1, relief='solid', padx=5, pady=5)
        frame.pack(fill='x', pady=5)
        self.create_labeled_entry(frame, self.languages[self.current_language]["company"], exp['company'], lambda val: self.on_experience_change('professional_experience', index, 'company', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["position"], exp['position'], lambda val: self.on_experience_change('professional_experience', index, 'position', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["start_date"], exp['start_date'], lambda val: self.on_experience_change('professional_experience', index, 'start_date', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["end_date"], exp['end_date'], lambda val: self.on_experience_change('professional_experience', index, 'end_date', val))
        self.create_labeled_entry(frame, self.languages[self.current_language]["description"], exp.get('description', ''), lambda val: self.on_experience_change('professional_experience', index, 'description', val))
        tk.Button(frame, text=self.languages[self.current_language]["remove"], command=lambda: self.remove_experience('professional_experience', index)).pack(anchor='e')

    def create_labeled_entry(self, parent, label_text, value, on_change):
        """Creates a labeled entry field."""
        frame = tk.Frame(parent)
        frame.pack(anchor='w', pady=2)
        tk.Label(frame, text=label_text + ":", width=12, anchor='w').pack(side='left')
        entry = tk.Entry(frame)
        entry.pack(side='left', fill='x', expand=True)
        entry.insert(0, value)
        entry.bind("<FocusOut>", lambda e: on_change(entry.get()))

    def set_data_modified(self, modified=True):
        """Sets the data modified flag."""
        self.is_data_modified = modified

    def save_data_from_preview(self):
        """Saves data from the preview to the JSON file."""
        if self.is_data_modified:
            try:
                with open(self.data_file, "w") as f:
                    data = {
                        "name": self.name.get(), "title": self.title.get(), "summary": self.summary.get(),
                        "phone": self.phone.get(), "age": self.age.get(), "city": self.city.get(),
                        "foto_encoded": self.foto_encoded, "mostrar_foto": self.mostrar_foto.get(),
                        "professional_experience": self.professional_experience,
                        "academic_experience": self.academic_experience, "skills": self.skills,
                        "certificates": self.certificates
                    }
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Saved", "Your changes have been saved successfully!")
                self.is_data_modified = False
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving: {str(e)}")
        else:
            messagebox.showinfo("No Changes", "No changes to save.")

    def generate_curriculum(self):
        """Generates the curriculum as an HTML file and opens it in a web browser."""
        html = self.render_html()
        timestamp_hex = hex(int(time.time()))[2:].upper()  # Convert timestamp to hexadecimal
        filename = f"curriculum-{self.current_language}-{timestamp_hex}.html"
        try:
            with open(filename, "w", encoding='utf-8') as f:
                f.write(html)
            webbrowser.open(filename)
        except Exception as e:
            messagebox.showerror("Generate Error", f"An error occurred while generating the CV: {str(e)}")

    def render_html(self):
        """Renders the curriculum as an HTML string using a Jinja2 template."""
        template = Template("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ labels.curriculum }}</title>
            <style>
                @page {
                    size: A4;
                    margin: 20mm;
                }
                body {
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    background-color: #f5f5f5;
                    color: #333;
                    text-align: left;
                    width: 210mm;
                    margin: 15mm auto;
                    background-color: white;
                    padding: 10mm;
                    -webkit-box-shadow: 0 2px 4px rgba(0, 0, 0, .1);
                    -moz-box-shadow: 0 2px 4px rgba(0, 0, 0, .1);
                    box-shadow: 0 2px 4px rgba(0, 0, 0, .1);
                }
                @media print {
                    body {
                        margin: 0;
                        font-size: 12pt;
                        background-color: white;
                        -webkit-box-shadow:none;
                        -moz-box-shadow:none;
                        box-shadow:none;
                        padding:0;
                    }
                    header, section {
                        page-break-after: auto;
                    }
                }
                header, section {
                    page-break-after: avoid;
                    page-break-inside: avoid;
                }
                header {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    margin-bottom: 20px;
                }
                header div {
                    width: 100%;
                }
                header img {
                    border-radius: 50%;
                    margin-right: 20px;
                    width: 100px;
                    height: 100px;
                }
                header h1 {
                    margin: 0;
                    font-size: 28px;
                }
                header h2 {
                    margin-top: 0.25em;
                }
                header p {
                    margin-bottom: 0;
                }
                section {
                    margin-bottom: 20px;
                    text-align: left;
                }
                h2, h3 {
                    page-break-after: avoid;
                }
                h2 {
                    font-size: 22px;
                    color: midnightblue;
                    margin-bottom: 0;
                }
                h3 {
                    font-size: 18px;
                    border-bottom: 2px solid #333;
                    padding-bottom: 5px;
                    margin-bottom: 15px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <header>
                {% if mostrar_foto and foto %}
                <img src="{{ foto }}" alt="{{ labels.photo }}" style="width: 100px; height: 100px;">
                {% endif %}
                <div>
                    <h1>{{ name }}</h1>
                    {% if title %}<h2>{{ title }}</h2>{% endif %}
                    <p>{{ labels.phone }}: {{ phone }}{% if age %} | {{ labels.age }}: {{ age }}{% endif %}{% if city %} | {{ labels.city }}: {{ city }}{% endif %}</p>
                </div>
            </header>
            <section>
                <h3>{{ labels.summary }}</h3>
                <p>{{ summary }}</p>
            </section>
            <section>
                <h3>{{ labels.professional_experience }}</h3>
                <ul>
                    {% for experience in professional_experience %}
                    <li><b>{{ experience.company }} ({{ experience.start_date }} - {{ experience.end_date }}): {{ experience.position }}</b> <br> {{ experience.description }}</li>
                    {% endfor %}
                </ul>
            </section>
            <section>
                <h3>{{ labels.academic_experience }}</h3>
                <ul>
                    {% for experience in academic_experience %}
                    <li>{{ experience.institution }} ({{ experience.start_date }} - {{ experience.end_date }}): {{ experience.degree }}</li>
                    {% endfor %}
                </ul>
            </section>
            <section>
                <h3>{{ labels.skills }}</h3>
                <ul>
                    {% for skill in skills %}
                    <li>{{ skill }}</li>
                    {% endfor %}
                </ul>
            </section>
            <section>
                <h3>{{ labels.certificates }}</h3>
                <ul>
                    {% for certificate in certificates %}
                    <li>{{ certificate.name }} ({{ certificate.institution }} - {{ certificate.date }})</li>
                    {% endfor %}
                </ul>
            </section>
        </body>
        </html>
        """)

        labels = self.languages[self.current_language]
        labels['curriculum'] = 'Curriculum Vitae'

        return template.render(
            lang=self.current_language, labels=labels, 
            foto=self.foto_encoded, mostrar_foto=self.mostrar_foto.get(),
            name=self.name.get(), title=self.title.get(), summary=self.summary.get(),
            phone=self.phone.get(), age=self.age.get(), city=self.city.get(),
            professional_experience=self.professional_experience,
            academic_experience=self.academic_experience,
            skills=self.skills, certificates=self.certificates
        )

if __name__ == "__main__":
    curriculum = Curriculum()
    curriculum.root.mainloop()
