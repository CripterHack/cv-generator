import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { CVPreview } from '../CVPreview';
import { CVService } from '../../services/CVService';

jest.mock('../../services/CVService');

describe('CVPreview', () => {
  const mockData = {
    name: 'John Doe',
    title: 'Software Engineer',
    show_photo: false,
    professional_experience: [],
    academic_experience: [],
    skills: [],
    certificates: []
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('muestra el indicador de carga inicialmente', () => {
    render(<CVPreview data={mockData} template="modern" />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('muestra la vista previa cuando se genera exitosamente', async () => {
    const mockHtml = '<div>CV Preview Content</div>';
    jest.spyOn(CVService, 'generateCV').mockResolvedValueOnce({ html: mockHtml });

    render(<CVPreview data={mockData} template="modern" />);

    await waitFor(() => {
      expect(screen.getByText('CV Preview Content')).toBeInTheDocument();
    });
  });

  it('muestra mensaje de error cuando falla la generación', async () => {
    jest.spyOn(CVService, 'generateCV').mockRejectedValueOnce(new Error('API Error'));

    render(<CVPreview data={mockData} template="modern" />);

    await waitFor(() => {
      expect(screen.getByText(/error generating cv/i)).toBeInTheDocument();
    });
  });
}); 