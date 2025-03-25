# Frontend Documentation

## Component Library

Our component library is documented using Storybook, which provides an interactive environment to explore and test components in isolation.

### Running Storybook

```bash
# Start Storybook development server
npm run storybook

# Build static documentation
npm run build-storybook
```

Visit `http://localhost:6006` to view the component library.

## Component Structure

### Core Components

#### CVForm
Main form component for CV creation.

```typescript
import { CVForm } from '@components/CVForm';

<CVForm
  initialData={cvData}
  onSubmit={handleSubmit}
  onSave={handleSave}
/>
```

**Props:**
- `initialData`: Initial CV data
- `onSubmit`: Callback for form submission
- `onSave`: Callback for saving draft

#### CVPreview
Real-time preview of the CV.

```typescript
import { CVPreview } from '@components/CVPreview';

<CVPreview data={cvData} template="modern" />
```

**Props:**
- `data`: CV data to display
- `template`: Template name to use

### Form Sections

#### PersonalInfo
Personal information form section.

```typescript
import { PersonalInfo } from '@components/sections/PersonalInfo';

<PersonalInfo
  data={personalData}
  onChange={handleChange}
/>
```

#### ExperienceSection
Professional experience form section.

```typescript
import { ExperienceSection } from '@components/sections/ExperienceSection';

<ExperienceSection
  experiences={experiences}
  onChange={handleChange}
/>
```

## State Management

### CV Data Structure

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

### Form Validation

We use Yup for form validation:

```typescript
const validationSchema = yup.object({
  name: yup.string().required('Name is required'),
  title: yup.string().required('Title is required'),
  phone: yup.string().matches(/^\+?[\d\s-]+$/, 'Invalid phone number'),
  age: yup.number().min(16).max(100),
  // ... more validations
});
```

## Styling

### Theme Configuration

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

### CSS Modules

Example of component-specific styles:

```typescript
// CVForm.module.css
.container {
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

// Usage in component
import styles from './CVForm.module.css';

<div className={styles.container}>
  {/* Component content */}
</div>
```

## Internationalization

### Using Translations

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <h1>{t('form.personalInfo')}</h1>
  );
}
```

### Adding New Translations

Add translations to the respective language files:

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

## Testing

### Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CVForm } from './CVForm';

describe('CVForm', () => {
  it('renders all form fields', () => {
    render(<CVForm />);
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
  });

  it('handles form submission', async () => {
    const handleSubmit = jest.fn();
    render(<CVForm onSubmit={handleSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    expect(handleSubmit).toHaveBeenCalled();
  });
});
```

## Build and Deployment

### Production Build
```bash
# Build for production
npm run build

# Verify build locally
npm run serve
```

### Deployment Process
1. Run tests and linting
   ```bash
   npm run ci
   ```
2. Build the application
   ```bash
   npm run build:prod
   ```
3. Deploy the `build` directory to your hosting service

## Client-Side Caching

The frontend implements a caching strategy for:

### Form Data
- Uses localStorage to persist form state
- Autosaves every 30 seconds
- Clears on successful submission

### API Responses
- In-memory cache for API responses
- Cache invalidation on data updates
- Configurable TTL per endpoint

### Static Assets
- Service worker for offline support
- Cache static assets (images, styles, scripts)
- Automatic cache invalidation on new version

## Best Practices

1. **Component Organization**
   - One component per file
   - Group related components in folders
   - Use index.ts for exports

2. **Type Safety**
   - Define interfaces for all props
   - Use strict TypeScript settings
   - Avoid using `any`

3. **Performance**
   - Use React.memo for expensive renders
   - Implement proper dependency arrays in hooks
   - Lazy load components when possible

4. **Error Handling**
   - Implement error boundaries
   - Provide meaningful error messages
   - Log errors appropriately

5. **Accessibility**
   - Use semantic HTML
   - Include ARIA labels
   - Ensure keyboard navigation works 