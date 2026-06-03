import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CVForm } from '../CVForm';

jest.mock('../../services/CVService');

describe('CVForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    expect(screen.getByLabelText(/nombre completo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/teléfono/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/resumen profesional/i)).toBeInTheDocument();
  });

  it('updates form data on input change', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const nameInput = screen.getByLabelText(/nombre completo/i);
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    expect(nameInput).toHaveValue('John Doe');

    const emailInput = screen.getByLabelText(/email/i);
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    expect(emailInput).toHaveValue('john@example.com');
  });

  it('submits form with valid data', async () => {
    const mockOnSubmit = jest.fn();
    render(<CVForm onSubmit={mockOnSubmit} />);

    fireEvent.change(screen.getByLabelText(/nombre completo/i), {
      target: { value: 'John Doe' },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' },
    });

    const submitButton = screen.getByRole('button', { name: /crear cv/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          fullName: 'John Doe',
          email: 'john@example.com',
        }),
      );
    });
  });

  it('handles photo upload', async () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const file = new File(['photo'], 'photo.png', { type: 'image/png' });
    const input = screen.getByLabelText(/subir foto/i);

    Object.defineProperty(input, 'files', {
      value: [file],
    });

    fireEvent.change(input);

    await waitFor(() => {
      expect(screen.getByRole('img')).toBeInTheDocument();
    });
  });

  it('adds education fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const addButton = screen.getByRole('button', { name: /agregar educación/i });
    fireEvent.click(addButton);

    const institutionInputs = screen.getAllByLabelText(/institución/i);
    expect(institutionInputs.length).toBe(2);
  });

  it('adds experience fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const addButton = screen.getByRole('button', { name: /agregar experiencia/i });
    fireEvent.click(addButton);

    const companyInputs = screen.getAllByLabelText(/empresa/i);
    expect(companyInputs.length).toBe(2);
  });

  it('adds skill fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const addButton = screen.getByRole('button', { name: /agregar habilidad/i });
    fireEvent.click(addButton);

    const skillInputs = screen.getAllByLabelText(/habilidad/i);
    expect(skillInputs.length).toBe(2);
  });

  it('adds certificate fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const addButton = screen.getByRole('button', { name: /agregar certificado/i });
    fireEvent.click(addButton);

    const certInputs = screen.getAllByLabelText(/nombre del certificado/i);
    expect(certInputs.length).toBe(1);
  });

  it('adds language fields', () => {
    render(<CVForm onSubmit={jest.fn()} />);

    const addButton = screen.getByRole('button', { name: /agregar idioma/i });
    fireEvent.click(addButton);

    const langInputs = screen.getAllByLabelText(/idioma/i);
    expect(langInputs.length).toBe(1);
  });
});
