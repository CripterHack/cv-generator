# Documentación del Frontend

## Biblioteca de Componentes

Nuestra biblioteca de componentes está documentada usando Storybook, que proporciona un entorno interactivo para explorar y probar componentes de forma aislada.

### Ejecutar Storybook

```bash
# Iniciar servidor de desarrollo de Storybook
npm run storybook

# Construir documentación estática
npm run build-storybook
```

Visita `http://localhost:6006` para ver la biblioteca de componentes.

## Estructura de Componentes

### Componentes Principales

#### CVForm
Componente principal del formulario para la creación de CV.

```typescript
import { CVForm } from '@components/CVForm';

<CVForm
  initialData={cvData}
  onSubmit={handleSubmit}
  onSave={handleSave}
/>
```

**Props:**
- `initialData`: Datos iniciales del CV
- `onSubmit`: Callback para el envío del formulario
- `onSave`: Callback para guardar borrador

#### CVPreview
Vista previa en tiempo real del CV.

```typescript
import { CVPreview } from '@components/CVPreview';

<CVPreview data={cvData} template="modern" />
```

**Props:**
- `data`: Datos del CV a mostrar
- `template`: Nombre de la plantilla a usar

### Secciones del Formulario

#### PersonalInfo
Sección de información personal del formulario.

```typescript
import { PersonalInfo } from '@components/sections/PersonalInfo';

<PersonalInfo
  data={personalData}
  onChange={handleChange}
/>
```

#### ExperienceSection
Sección de experiencia profesional del formulario.

```typescript
import { ExperienceSection } from '@components/sections/ExperienceSection';

<ExperienceSection
  experiences={experiences}
  onChange={handleChange}
/>
```

## Gestión del Estado

### Estructura de Datos del CV

```typescript
interface CV {
  name: string;
  title: string;
  phone?: string;
  age?: number;
  city?: string;
  summary?: string;
  photo_base64?: string;
  show_photo: boolean;
  professional_experience: Experience[];
  academic_experience: Education[];
  skills: string[];
  certificates: Certificate[];
}
```

### Validación de Formularios

Usamos Yup para la validación de formularios:

```typescript
const validationSchema = yup.object({
  name: yup.string().required('El nombre es requerido'),
  title: yup.string().required('El título es requerido'),
  phone: yup.string().matches(/^\+?[\d\s-]+$/, 'Número de teléfono inválido'),
  age: yup.number().min(16).max(100),
  // ... más validaciones
});
```

## Estilos

### Configuración del Tema

```typescript
const theme = createTheme({
  palette: {
    primary: {
      main: '#2292a7'
    },
    secondary: {
      main: '#f50057'
    }
  },
  typography: {
    fontFamily: 'Open Sans, Arial, sans-serif'
  }
});
```

### Módulos CSS

Ejemplo de estilos específicos de componentes:

```typescript
// CVForm.module.css
.container {
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

// Uso en el componente
import styles from './CVForm.module.css';

<div className={styles.container}>
  {/* Contenido del componente */}
</div>
```

## Internacionalización

### Uso de Traducciones

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <h1>{t('form.personalInfo')}</h1>
  );
}
```

### Agregar Nuevas Traducciones

Agregar traducciones a los archivos de idioma respectivos:

```typescript
// src/i18n/locales/en.json
{
  "form": {
    "personalInfo": "Personal Information"
  }
}

// src/i18n/locales/es.json
{
  "form": {
    "personalInfo": "Información Personal"
  }
}
```

## Pruebas

### Pruebas de Componentes

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CVForm } from './CVForm';

describe('CVForm', () => {
  it('renderiza todos los campos del formulario', () => {
    render(<CVForm />);
    expect(screen.getByLabelText(/nombre/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/título/i)).toBeInTheDocument();
  });

  it('maneja el envío del formulario', async () => {
    const handleSubmit = jest.fn();
    render(<CVForm onSubmit={handleSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/nombre/i), {
      target: { value: 'Juan Pérez' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));
    expect(handleSubmit).toHaveBeenCalled();
  });
});
```

## Build y Despliegue

### Build de Producción
```bash
# Construir para producción
npm run build

# Verificar build localmente
npm run serve
```

### Proceso de Despliegue
1. Ejecutar pruebas y linting
   ```bash
   npm run ci
   ```
2. Construir la aplicación
   ```bash
   npm run build:prod
   ```
3. Desplegar el directorio `build` a tu servicio de hosting

## Caché del Cliente

El frontend implementa una estrategia de caché para:

### Datos del Formulario
- Usa localStorage para persistir el estado del formulario
- Autoguardado cada 30 segundos
- Se limpia después de un envío exitoso

### Respuestas de la API
- Caché en memoria para respuestas de la API
- Invalidación de caché en actualizaciones de datos
- TTL configurable por endpoint

### Recursos Estáticos
- Service worker para soporte offline
- Caché de recursos estáticos (imágenes, estilos, scripts)
- Invalidación automática de caché en nueva versión

## Mejores Prácticas

1. **Organización de Componentes**
   - Un componente por archivo
   - Agrupar componentes relacionados en carpetas
   - Usar index.ts para exportaciones

2. **Seguridad de Tipos**
   - Definir interfaces para todas las props
   - Usar configuración estricta de TypeScript
   - Evitar usar `any`

3. **Rendimiento**
   - Usar React.memo para renderizados costosos
   - Implementar arrays de dependencias adecuados en hooks
   - Cargar componentes de forma perezosa cuando sea posible

4. **Manejo de Errores**
   - Implementar límites de error
   - Proporcionar mensajes de error significativos
   - Registrar errores apropiadamente

5. **Accesibilidad**
   - Usar HTML semántico
   - Incluir etiquetas ARIA
   - Asegurar que funciona la navegación por teclado 