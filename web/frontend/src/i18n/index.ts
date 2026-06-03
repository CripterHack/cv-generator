import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      es: {
        translation: {
          'Crear nuevo CV': 'Crear nuevo CV',
          'Nombre completo': 'Nombre completo',
          'Email': 'Email',
          'Teléfono': 'Teléfono',
          'Resumen profesional': 'Resumen profesional',
          'Subir foto': 'Subir foto',
          'Crear CV': 'Crear CV',
          'CV creado exitosamente': 'CV creado exitosamente',
          'Error al crear el CV': 'Error al crear el CV',
          'Experiencia profesional': 'Experiencia profesional',
          'Educación': 'Educación',
          'Habilidades': 'Habilidades',
          'Certificados': 'Certificados',
          'Agregar experiencia': 'Agregar experiencia',
          'Agregar educación': 'Agregar educación',
          'Agregar habilidad': 'Agregar habilidad',
          'Agregar certificado': 'Agregar certificado',
          'Guardar': 'Guardar',
          'Cancelar': 'Cancelar',
          'Eliminar': 'Eliminar',
          'Presente': 'Presente',
          'Fecha inicio': 'Fecha inicio',
          'Fecha fin': 'Fecha fin',
          'Empresa': 'Empresa',
          'Puesto': 'Puesto',
          'Descripción': 'Descripción',
          'Institución': 'Institución',
          'Título': 'Título',
          'Área de estudio': 'Área de estudio'
        }
      },
      en: {
        translation: {
          'Crear nuevo CV': 'Create new CV',
          'Nombre completo': 'Full name',
          'Email': 'Email',
          'Teléfono': 'Phone',
          'Resumen profesional': 'Professional summary',
          'Subir foto': 'Upload photo',
          'Crear CV': 'Create CV',
          'CV creado exitosamente': 'CV created successfully',
          'Error al crear el CV': 'Error creating CV',
          'Experiencia profesional': 'Professional experience',
          'Educación': 'Education',
          'Habilidades': 'Skills',
          'Certificados': 'Certificates',
          'Agregar experiencia': 'Add experience',
          'Agregar educación': 'Add education',
          'Agregar habilidad': 'Add skill',
          'Agregar certificado': 'Add certificate',
          'Guardar': 'Save',
          'Cancelar': 'Cancel',
          'Eliminar': 'Delete',
          'Presente': 'Present',
          'Fecha inicio': 'Start date',
          'Fecha fin': 'End date',
          'Empresa': 'Company',
          'Puesto': 'Position',
          'Descripción': 'Description',
          'Institución': 'Institution',
          'Título': 'Degree',
          'Área de estudio': 'Field of study'
        }
      }
    },
    fallbackLng: 'es',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n; 