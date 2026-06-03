import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Grid,
  Paper,
  Typography,
  Snackbar,
  IconButton,
} from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import { PhotoCamera, Delete } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { CVData } from '../types/cv';
import jsPDF from 'jspdf';
import showdown from 'showdown';

interface CVFormProps {
  onSubmit: (data: CVData) => void;
}

export const CVForm: React.FC<CVFormProps> = ({ onSubmit }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState<CVData>({
    fullName: '',
    email: '',
    phone: '',
    summary: '',
    education: [{ institution: '', degree: '', fieldOfStudy: '', startDate: '', endDate: '' }],
    experience: [{ company: '', position: '', startDate: '', endDate: '', description: '' }],
    skills: [{ name: '', level: 0 }]
  });
  const [photo, setPhoto] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhoto(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      onSubmit(formData);
      setSnackbar({
        open: true,
        message: t('CV creado exitosamente'),
        severity: 'success',
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: t('Error al crear el CV'),
        severity: 'error',
      });
    }
  };

  const exportToJson = () => {
    const dataStr = JSON.stringify(formData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'cv.json';
    link.click();
  };

  const exportToPdf = () => {
    const doc = new jsPDF();
    doc.text(`Name: ${formData.fullName}`, 10, 10);
    doc.text(`Email: ${formData.email}`, 10, 20);
    // Add more fields as needed
    doc.save('cv.pdf');
  };

  const exportToMarkdown = () => {
    const converter = new showdown.Converter();
    const markdown = converter.makeHtml(`## ${formData.fullName}\n${formData.summary}`);
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'cv.md';
    link.click();
  };

  const exportToHtml = () => {
    const htmlContent = `<h1>${formData.fullName}</h1><p>${formData.summary}</p>`;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'cv.html';
    link.click();
  };

  const handleJsonUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        const json = JSON.parse(event.target?.result as string);
        setFormData(json);
      };
      reader.readAsText(file);
    }
  };

  const handleAddEducation = () => {
    setFormData((prev) => ({
      ...prev,
      education: [...prev.education, { institution: '', degree: '', fieldOfStudy: '', startDate: '', endDate: '' }]
    }));
  };

  const handleAddExperience = () => {
    setFormData((prev) => ({
      ...prev,
      experience: [...prev.experience, { company: '', position: '', startDate: '', endDate: '', description: '' }]
    }));
  };

  const handleAddSkill = () => {
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, { name: '', level: 0 }]
    }));
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
              {t('Crear nuevo CV')}
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              name="fullName"
              label={t('Nombre completo')}
              value={formData.fullName}
              onChange={handleInputChange}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              type="email"
              name="email"
              label={t('Email')}
              value={formData.email}
              onChange={handleInputChange}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              name="phone"
              label={t('Teléfono')}
              value={formData.phone}
              onChange={handleInputChange}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              name="summary"
              label={t('Resumen profesional')}
              value={formData.summary}
              onChange={handleInputChange}
            />
          </Grid>

          <Grid item xs={12}>
            <Box display="flex" alignItems="center" gap={2}>
              <input
                accept="image/*"
                style={{ display: 'none' }}
                id="photo-upload"
                type="file"
                onChange={handlePhotoUpload}
              />
              <label htmlFor="photo-upload">
                <Button
                  variant="contained"
                  component="span"
                  startIcon={<PhotoCamera />}
                >
                  {t('Subir foto')}
                </Button>
              </label>
              {photo && (
                <IconButton onClick={() => setPhoto(null)} color="error">
                  <Delete />
                </IconButton>
              )}
            </Box>
            {photo && (
              <Box mt={2}>
                <img
                  src={photo}
                  alt="Preview"
                  style={{ width: 150, height: 150, objectFit: 'cover' }}
                />
              </Box>
            )}
          </Grid>

          <Grid item xs={12}>
            <Typography variant="h6">{t('Educación')}</Typography>
            {formData.education.map((edu, index) => (
              <Box key={index} mb={2}>
                <TextField
                  fullWidth
                  label={t('Institución')}
                  value={edu.institution}
                  onChange={(e) => {
                    const newEducation = [...formData.education];
                    newEducation[index].institution = e.target.value;
                    setFormData((prev) => ({ ...prev, education: newEducation }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Título')}
                  value={edu.degree}
                  onChange={(e) => {
                    const newEducation = [...formData.education];
                    newEducation[index].degree = e.target.value;
                    setFormData((prev) => ({ ...prev, education: newEducation }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Campo de estudio')}
                  value={edu.fieldOfStudy}
                  onChange={(e) => {
                    const newEducation = [...formData.education];
                    newEducation[index].fieldOfStudy = e.target.value;
                    setFormData((prev) => ({ ...prev, education: newEducation }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Fecha de inicio')}
                  value={edu.startDate}
                  onChange={(e) => {
                    const newEducation = [...formData.education];
                    newEducation[index].startDate = e.target.value;
                    setFormData((prev) => ({ ...prev, education: newEducation }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Fecha de fin')}
                  value={edu.endDate}
                  onChange={(e) => {
                    const newEducation = [...formData.education];
                    newEducation[index].endDate = e.target.value;
                    setFormData((prev) => ({ ...prev, education: newEducation }));
                  }}
                />
              </Box>
            ))}
            <Button onClick={handleAddEducation} variant="outlined">{t('Agregar Educación')}</Button>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="h6">{t('Experiencia Profesional')}</Typography>
            {formData.experience.map((exp, index) => (
              <Box key={index} mb={2}>
                <TextField
                  fullWidth
                  label={t('Empresa')}
                  value={exp.company}
                  onChange={(e) => {
                    const newExperience = [...formData.experience];
                    newExperience[index].company = e.target.value;
                    setFormData((prev) => ({ ...prev, experience: newExperience }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Puesto')}
                  value={exp.position}
                  onChange={(e) => {
                    const newExperience = [...formData.experience];
                    newExperience[index].position = e.target.value;
                    setFormData((prev) => ({ ...prev, experience: newExperience }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Fecha de inicio')}
                  value={exp.startDate}
                  onChange={(e) => {
                    const newExperience = [...formData.experience];
                    newExperience[index].startDate = e.target.value;
                    setFormData((prev) => ({ ...prev, experience: newExperience }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Fecha de fin')}
                  value={exp.endDate}
                  onChange={(e) => {
                    const newExperience = [...formData.experience];
                    newExperience[index].endDate = e.target.value;
                    setFormData((prev) => ({ ...prev, experience: newExperience }));
                  }}
                />
                <TextField
                  fullWidth
                  multiline
                  rows={2}
                  label={t('Descripción')}
                  value={exp.description}
                  onChange={(e) => {
                    const newExperience = [...formData.experience];
                    newExperience[index].description = e.target.value;
                    setFormData((prev) => ({ ...prev, experience: newExperience }));
                  }}
                />
              </Box>
            ))}
            <Button onClick={handleAddExperience} variant="outlined">{t('Agregar Experiencia')}</Button>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="h6">{t('Habilidades')}</Typography>
            {formData.skills.map((skill, index) => (
              <Box key={index} mb={2}>
                <TextField
                  fullWidth
                  label={t('Habilidad')}
                  value={skill.name}
                  onChange={(e) => {
                    const newSkills = [...formData.skills];
                    newSkills[index].name = e.target.value;
                    setFormData((prev) => ({ ...prev, skills: newSkills }));
                  }}
                />
                <TextField
                  fullWidth
                  label={t('Nivel')}
                  type="number"
                  value={skill.level}
                  onChange={(e) => {
                    const newSkills = [...formData.skills];
                    newSkills[index].level = parseInt(e.target.value, 10);
                    setFormData((prev) => ({ ...prev, skills: newSkills }));
                  }}
                />
              </Box>
            ))}
            <Button onClick={handleAddSkill} variant="outlined">{t('Agregar Habilidad')}</Button>
          </Grid>

          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary">
              {t('Crear CV')}
            </Button>
          </Grid>

          <Grid item xs={12}>
            <Button onClick={exportToJson} variant="contained" color="secondary">
              {t('Exportar a JSON')}
            </Button>
            <Button onClick={exportToPdf} variant="contained" color="secondary">
              {t('Exportar a PDF')}
            </Button>
            <Button onClick={exportToMarkdown} variant="contained" color="secondary">
              {t('Exportar a Markdown')}
            </Button>
            <Button onClick={exportToHtml} variant="contained" color="secondary">
              {t('Exportar a HTML')}
            </Button>
            <input
              accept=".json"
              style={{ display: 'none' }}
              id="json-upload"
              type="file"
              onChange={handleJsonUpload}
            />
            <label htmlFor="json-upload">
              <Button variant="contained" component="span" color="secondary">
                {t('Cargar JSON')}
              </Button>
            </label>
          </Grid>
        </Grid>
      </form>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <MuiAlert
          elevation={6}
          variant="filled"
          severity={snackbar.severity}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          {snackbar.message}
        </MuiAlert>
      </Snackbar>
    </Paper>
  );
}; 