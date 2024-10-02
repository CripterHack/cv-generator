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

- Python 3.x
- Tkinter
- Pillow
- Jinja2
- pdfkit
- markdown2
- reportlab

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

### Tested Functionalities:
- CV creation and editing
- Exporting to HTML, PDF, and Markdown
- Saving and loading JSON data
- Importing JSON data
- Bilingual switching

### To Be Tested:
- Performance with very large CVs
- Compatibility with older Python versions
- Behavior on low-resource systems
- Cross-platform executable creation
- Profile photo styling

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Special thanks to the developers of the libraries used in this project.
