import React from 'react';
import { Box, Paper, Typography, CircularProgress } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { CVData } from '../types/cv';

interface CVPreviewProps {
  data?: CVData | null;
  loading?: boolean;
}

export const CVPreview: React.FC<CVPreviewProps> = ({ data, loading = false }) => {
  const { t } = useTranslation();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (!data) {
    return (
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="body1" color="textSecondary" align="center">
          {t('No hay datos para previsualizar')}
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        {data.fullName}
      </Typography>
      
      <Typography variant="body1" color="textSecondary" gutterBottom>
        {data.email}
        {data.phone && ` • ${data.phone}`}
      </Typography>

      {data.summary && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            {t('Resumen')}
          </Typography>
          <Typography variant="body1">{data.summary}</Typography>
        </Box>
      )}

      {data.experience.length > 0 && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            {t('Experiencia')}
          </Typography>
          {data.experience.map((exp, index) => (
            <Box key={index} mb={2}>
              <Typography variant="subtitle1" fontWeight="bold">
                {exp.position} - {exp.company}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {exp.startDate} - {exp.endDate || t('Presente')}
              </Typography>
              {exp.description && (
                <Typography variant="body2">{exp.description}</Typography>
              )}
            </Box>
          ))}
        </Box>
      )}

      {data.education.length > 0 && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            {t('Educación')}
          </Typography>
          {data.education.map((edu, index) => (
            <Box key={index} mb={2}>
              <Typography variant="subtitle1" fontWeight="bold">
                {edu.degree} - {edu.fieldOfStudy}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {edu.institution}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {edu.startDate} - {edu.endDate || t('Presente')}
              </Typography>
              {edu.description && (
                <Typography variant="body2">{edu.description}</Typography>
              )}
            </Box>
          ))}
        </Box>
      )}

      {data.skills.length > 0 && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            {t('Habilidades')}
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {data.skills.map((skill, index) => (
              <Typography
                key={index}
                variant="body2"
                sx={{
                  bgcolor: 'primary.main',
                  color: 'white',
                  px: 1,
                  py: 0.5,
                  borderRadius: 1,
                }}
              >
                {skill.name}
                {skill.level && ` (${skill.level})`}
              </Typography>
            ))}
          </Box>
        </Box>
      )}
    </Paper>
  );
};