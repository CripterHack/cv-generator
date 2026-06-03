import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import { useTranslation } from 'react-i18next';
import theme from './theme';
import { CVForm } from './components/CVForm';
import { CVPreview } from './components/CVPreview';
import { CVData } from './types/cv';

function App() {
  const { t } = useTranslation();
  const [cvData, setCvData] = useState<CVData | null>(null);

  const handleCVSubmit = (data: CVData) => {
    setCvData(data);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h3" component="h1" gutterBottom>
            CV Generator
          </Typography>
          <Typography variant="h6" gutterBottom color="text.secondary">
            {t('Crea tu currículum vitae profesional')}
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <CVForm onSubmit={handleCVSubmit} />
          </Grid>
          <Grid item xs={12} md={6}>
            <CVPreview data={cvData} />
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App; 