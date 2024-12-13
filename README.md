# CV Generator 📄✨

CV Generator is a Python application that allows users to create, edit, and export professional curricula vitae (CVs) with ease. The application provides a user-friendly graphical interface for inputting personal information, work experience, education, skills, and certificates.

## Features 🌟

- Bilingual support (English and Spanish) 🌎
- Easy-to-use graphical user interface 🖥️
- Real-time preview of CV content 👀
- Export options:
  - HTML format 🌐
  - PDF format 📑
  - Markdown format ⬇️
- Save and load CV data in JSON format 💾
- Import previously saved CV data from JSON files 📤
- Customizable sections:
  - Personal Information 👤
  - Professional Experience 💼
  - Academic Experience 🎓
  - Skills 🛠️
  - Certificates 🏆
- Option to include a profile photo 🖼️

## Requirements 📋

- Python 3.11.5 (required)
- Tkinter (included with Python)
- Pillow>=9.5.0
- Jinja2>=3.1.2
- pdfkit>=1.0.0
- markdown2>=2.4.8
- reportlab>=3.6.12

## Python Version Compatibility ⚠️

This project is specifically designed to work with Python 3.11.5. Using other versions may lead to compatibility issues or unexpected behavior. We recommend using exactly this version for the best experience.

## Virtual Environment Setup 🔧

1. First, ensure you have Python 3.11.5 installed. You can check your Python version with:
   ```bash
   python --version
   ```

2. Install virtualenv if you haven't already:
   ```bash
   pip install virtualenv
   ```

3. Create a new virtual environment:
   ```bash
   # Windows
   python -m venv venv

   # Linux/Mac
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. When you're done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Installation 🚀

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cv-generator.git
   ```

2. Navigate to the project directory:
   ```
   cd cv-generator
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage 🔧

Run the application by executing the main Python script:
```
python cv_generator.py
```

The graphical interface will open, allowing you to input your CV information. Use the various buttons and fields to add your personal details, work experience, education, skills, and certificates.

## Exporting Your CV 📤

Once you've entered your information, you can export your CV in several formats:

- Click "Generate CV" to create an HTML version of your CV.
- Use "Export as PDF" to save your CV as a PDF file.
- Select "Export as Markdown" to get a Markdown version of your CV.

## Saving, Loading, and Importing Data 💾

- Click "Save Changes" to save your current CV data to a JSON file.
- Use "Load Data" to load previously saved CV information.
- Click "Import JSON" to import CV data from a previously saved JSON file.

## Creating an Executable 🖥️

To create an executable file from the Python script, follow these steps:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Navigate to the project directory:
   ```
   cd path/to/cv-generator
   ```

3. Run PyInstaller:
   ```
   pyinstaller --onefile --windowed cv-generator.py
   ```

4. Find the executable in the `dist` folder.

## To-Do List 📝

- [ ] Add support for more languages
- [ ] Implement custom CV templates
- [ ] Create a web-based version of the application
- [ ] Add integration with LinkedIn for easy data import
- [ ] Implement a spell-checker for CV content
- [ ] Add option to include QR code in CV
- [ ] Create a mobile app version
- [ ] Implement AI-powered CV suggestions
- [ ] Add support for video CVs
- [ ] Implement version control for CV edits
- [ ] Automatically language translation for the CV

## Testing 🧪

### Tested Environments:
- Windows 11, Python 3.11.5

### Unit Tests
- Run: `python -m unittest tests/`

### Tested Functionalities:
- CV creation and editing
- Exporting to HTML, PDF, and Markdown
- Saving and loading JSON data
- Importing JSON data
- Bilingual switching

### Integration Tests
- Verify PDF generation
- Validate JSON import/export
- Check data persistence

### To Be Tested:
- Performance with very large CVs
- Compatibility with older Python versions
- Behavior on low-resource systems
- Cross-platform executable creation
- Profile photo styling

### Code Coverage
- Use coverage.py: `coverage run -m unittest discover`
- Generate report: `coverage report`

## Common Issues and Solutions 🔨

### 1. ModuleNotFoundError: No module named 'tkinter'
**Solution:** Tkinter comes with Python but might need separate installation on Linux:
```bash
sudo apt-get install python3-tk
```

### 2. pdfkit Dependencies Error
**Solution:** Install wkhtmltopdf:
```bash
# Windows
# Download and install from: https://wkhtmltopdf.org/downloads.html

# Linux
sudo apt-get install wkhtmltopdf

# Mac
brew install wkhtmltopdf
```

### 3. Pillow Installation Issues
**Solution:** Install system dependencies first:
```bash
# Linux
sudo apt-get install python3-dev python3-setuptools libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk

# Then reinstall Pillow
pip uninstall Pillow
pip install Pillow
```

### 4. Virtual Environment Activation Fails
**Solution:** If you get permission errors:
```bash
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/Mac
chmod +x venv/bin/activate
```

## Project Architecture 🏗️

- `cv-generator.py`: Main file containing the application logic
- `curriculum_data.json`: Template file for storing CV data
- `requirements.txt`: Project dependencies
- `.devcontainer/`: Development container configuration

## Data Structure 📊

The CV is structured in the following main sections:
- Personal Information
- Professional Experience
- Academic Experience
- Skills and Abilities
- Certificates

Each section handles its own specific data format, documented in `curriculum_data.json`.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Special thanks to the developers of the libraries used in this project.
- Thanks to the open-source community for the tools and resources that made this project possible.
