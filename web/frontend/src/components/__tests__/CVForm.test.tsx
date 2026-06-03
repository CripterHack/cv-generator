import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CVForm } from '../CVForm';
import { CVService } from '../../services/CVService';

// Mock the CV service
jest.mock('../../services/CVService');

describe('CVForm', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(<CVForm />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/phone/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/city/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/summary/i)).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(<CVForm />);
    
    const submitButton = screen.getByRole('button', { name: /generate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    const mockGenerateCV = jest.spyOn(CVService, 'generateCV');
    mockGenerateCV.mockResolvedValueOnce({ success: true });

    render(<CVForm />);
    
    // Fill in form fields
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Software Engineer' }
    });

    // Submit form
    const submitButton = screen.getByRole('button', { name: /generate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockGenerateCV).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'John Doe',
          title: 'Software Engineer'
        })
      );
    });
  });

  it('handles photo upload', async () => {
    const mockUploadPhoto = jest.spyOn(CVService, 'uploadPhoto');
    mockUploadPhoto.mockResolvedValueOnce('photo-url');

    render(<CVForm />);
    
    const file = new File(['photo'], 'photo.png', { type: 'image/png' });
    const input = screen.getByLabelText(/photo/i);
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);

    await waitFor(() => {
      expect(mockUploadPhoto).toHaveBeenCalledWith(file);
    });
  });

  it('handles API errors gracefully', async () => {
    const mockGenerateCV = jest.spyOn(CVService, 'generateCV');
    mockGenerateCV.mockRejectedValueOnce(new Error('API Error'));

    render(<CVForm />);
    
    // Fill in required fields
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Software Engineer' }
    });

    // Submit form
    const submitButton = screen.getByRole('button', { name: /generate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/error generating cv/i)).toBeInTheDocument();
    });
  });
}); 