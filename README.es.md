# Generador de CV 📄✨

Generador de CV es una aplicación Python que permite a los usuarios crear, editar y exportar currículum vitae (CV) profesionales de manera sencilla. La aplicación proporciona una interfaz gráfica intuitiva para introducir información personal, experiencia laboral, educación, habilidades y certificados.

## Características 🌟

- Soporte bilingüe (Inglés y Español) 🌎
- Interfaz gráfica fácil de usar 🖥️
- Vista previa en tiempo real del contenido del CV 👀
- Opciones de exportación:
  - Formato HTML 🌐
  - Formato PDF 📑
  - Formato Markdown ⬇️
- Guardar y cargar datos del CV en formato JSON 💾
- Importar datos de CV previamente guardados desde archivos JSON 📤
- Secciones personalizables:
  - Información Personal 👤
  - Experiencia Profesional 💼
  - Experiencia Académica 🎓
  - Habilidades 🛠️
  - Certificados 🏆
- Opción para incluir foto de perfil 🖼️

## Requisitos 📋

- Python 3.11.5 (requerido)
- Tkinter (incluido con Python)
- Pillow>=9.5.0
- Jinja2>=3.1.2
- pdfkit>=1.0.0
- markdown2>=2.4.8
- reportlab>=3.6.12

## Compatibilidad con Versiones de Python ⚠️

Este proyecto está específicamente diseñado para funcionar con Python 3.11.5. El uso de otras versiones puede provocar problemas de compatibilidad o comportamientos inesperados. Recomendamos usar exactamente esta versión para la mejor experiencia.

## Configuración del Entorno Virtual 🔧

1. Primero, asegúrate de tener Python 3.11.5 instalado. Puedes verificar tu versión de Python con:
   ```bash
   python --version
   ```

2. Instala virtualenv si aún no lo tienes:
   ```bash
   pip install virtualenv
   ```

3. Crea un nuevo entorno virtual:
   ```bash
   # Windows
   python -m venv venv

   # Linux/Mac
   python3 -m venv venv
   ```

4. Activa el entorno virtual:
   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

5. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

6. Cuando termines, desactiva el entorno virtual:
   ```bash
   deactivate
   ```

## Instalación 🚀

1. Clona este repositorio:
   ```
   git clone https://github.com/yourusername/cv-generator.git
   ```

2. Navega al directorio del proyecto:
   ```
   cd cv-generator
   ```

3. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

## Uso 🔧

Ejecuta la aplicación ejecutando el script principal de Python:
```
python cv_generator.py
```

Se abrirá la interfaz gráfica, permitiéndote introducir la información de tu CV. Utiliza los diversos botones y campos para añadir tus datos personales, experiencia laboral, educación, habilidades y certificados.

## Exportar tu CV 📤

Una vez que hayas introducido tu información, puedes exportar tu CV en varios formatos:

- Haz clic en "Generar CV" para crear una versión HTML de tu CV.
- Usa "Exportar como PDF" para guardar tu CV como archivo PDF.
- Selecciona "Exportar como Markdown" para obtener una versión Markdown de tu CV.

## Guardar, Cargar e Importar Datos 💾

- Haz clic en "Guardar Cambios" para guardar los datos actuales de tu CV en un archivo JSON.
- Usa "Cargar Datos" para cargar información de CV previamente guardada.
- Haz clic en "Importar JSON" para importar datos de CV desde un archivo JSON previamente guardado.

## Crear un Ejecutable 🖥️

Para crear un archivo ejecutable desde el script de Python, sigue estos pasos:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Navega al directorio del proyecto:
   ```
   cd ruta/hacia/cv-generator
   ```

3. Ejecuta PyInstaller:
   ```
   pyinstaller --onefile --windowed cv-generator.py
   ```

4. Encuentra el ejecutable en la carpeta `dist`.

## Lista de Tareas Pendientes 📝

- [ ] Añadir soporte para más idiomas
- [ ] Implementar plantillas personalizadas de CV
- [ ] Crear una versión web de la aplicación
- [ ] Añadir integración con LinkedIn para importación fácil de datos
- [ ] Implementar un corrector ortográfico para el contenido del CV
- [ ] Añadir opción para incluir código QR en el CV
- [ ] Crear una versión para aplicación móvil
- [ ] Implementar sugerencias de CV basadas en IA
- [ ] Añadir soporte para CV en video
- [ ] Implementar control de versiones para ediciones de CV
- [ ] Traducción automática del CV

## Pruebas 🧪

### Entornos Probados:
- Windows 11, Python 3.11.5

### Pruebas Unitarias
- Ejecutar: `python -m unittest tests/`

### Funcionalidades Probadas:
- Creación y edición de CV
- Exportación a HTML, PDF y Markdown
- Guardado y carga de datos JSON
- Importación de datos JSON
- Cambio de idioma

### Pruebas de Integración
- Verificar generación de PDF
- Validar importación/exportación JSON
- Comprobar persistencia de datos

### Por Probar:
- Rendimiento con CV muy grandes
- Compatibilidad con versiones anteriores de Python
- Comportamiento en sistemas con recursos limitados
- Creación de ejecutables multiplataforma
- Estilizado de foto de perfil

### Cobertura de Código
- Usar coverage.py: `coverage run -m unittest discover`
- Generar informe: `coverage report`

## Problemas Comunes y Soluciones 🔨

### 1. ModuleNotFoundError: No module named 'tkinter'
**Solución:** Tkinter viene con Python pero puede necesitar instalación separada en Linux:
```bash
sudo apt-get install python3-tk
```

### 2. Error de Dependencias de pdfkit
**Solución:** Instalar wkhtmltopdf:
```bash
# Windows
# Descargar e instalar desde: https://wkhtmltopdf.org/downloads.html

# Linux
sudo apt-get install wkhtmltopdf

# Mac
brew install wkhtmltopdf
```

### 3. Problemas de Instalación de Pillow
**Solución:** Instalar primero las dependencias del sistema:
```bash
# Linux
sudo apt-get install python3-dev python3-setuptools libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk

# Luego reinstalar Pillow
pip uninstall Pillow
pip install Pillow
```

### 4. Fallo en la Activación del Entorno Virtual
**Solución:** Si tienes errores de permisos:
```bash
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/Mac
chmod +x venv/bin/activate
```

## Arquitectura del Proyecto 🏗️

- `cv-generator.py`: Archivo principal que contiene la lógica de la aplicación
- `curriculum_data.json`: Archivo plantilla para almacenar datos del CV
- `requirements.txt`: Dependencias del proyecto
- `.devcontainer/`: Configuración del contenedor de desarrollo

## Estructura de Datos 📊

El CV está estructurado en las siguientes secciones principales:
- Información Personal
- Experiencia Profesional
- Experiencia Académica
- Habilidades y Capacidades
- Certificados

Cada sección maneja su propio formato específico de datos, documentado en `curriculum_data.json`.

## Contribuir 🤝

¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request.

## Licencia 📜

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Agradecimientos 🙏

- Un agradecimiento especial a los desarrolladores de las bibliotecas utilizadas en este proyecto.
- Gracias a la comunidad de código abierto por las herramientas y recursos que hicieron posible este proyecto. 