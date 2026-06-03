import React from 'react';
import { render, screen } from '@testing-library/react';
import { CVPreview } from '../CVPreview';
import { CVData } from '../../types/cv';

describe('CVPreview', () => {
  const mockData: CVData = {
    fullName: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    summary: 'Experienced software engineer',
    education: [],
    experience: [],
    skills: [],
    certificates: [],
    languages: [],
  };

  it('shows empty state when no data provided', () => {
    render(<CVPreview data={null} />);
    expect(screen.getByText(/no hay datos para previsualizar/i)).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<CVPreview data={null} loading={true} />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders personal info', () => {
    render(<CVPreview data={mockData} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText(/john@example.com/)).toBeInTheDocument();
    expect(screen.getByText(/\+1234567890/)).toBeInTheDocument();
  });

  it('renders summary', () => {
    render(<CVPreview data={mockData} />);
    expect(screen.getByText('Experienced software engineer')).toBeInTheDocument();
  });

  it('renders experience', () => {
    const data: CVData = {
      ...mockData,
      experience: [
        {
          company: 'Tech Corp',
          position: 'Developer',
          startDate: '2020-01-01',
          endDate: '2023-12-31',
          description: 'Built things',
        },
      ],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('Developer - Tech Corp')).toBeInTheDocument();
    expect(screen.getByText('Built things')).toBeInTheDocument();
  });

  it('renders education', () => {
    const data: CVData = {
      ...mockData,
      education: [
        {
          institution: 'MIT',
          degree: 'BSc',
          fieldOfStudy: 'Computer Science',
          startDate: '2016-01-01',
          endDate: '2020-01-01',
        },
      ],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('BSc - Computer Science')).toBeInTheDocument();
    expect(screen.getByText('MIT')).toBeInTheDocument();
  });

  it('renders skills', () => {
    const data: CVData = {
      ...mockData,
      skills: [{ name: 'Python', level: 5 }],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('Python (5)')).toBeInTheDocument();
  });

  it('renders certificates', () => {
    const data: CVData = {
      ...mockData,
      certificates: [
        { name: 'AWS Certified', issuer: 'Amazon', dateObtained: '2023-01-01' },
      ],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('AWS Certified')).toBeInTheDocument();
    expect(screen.getByText(/Amazon.*2023-01-01/)).toBeInTheDocument();
  });

  it('renders languages', () => {
    const data: CVData = {
      ...mockData,
      languages: [{ name: 'Spanish', level: 'Native' }],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('Spanish (Native)')).toBeInTheDocument();
  });

  it('renders social links', () => {
    const data: CVData = {
      ...mockData,
      website: 'https://mysite.com',
      linkedin: 'https://linkedin.com/in/johndoe',
      github: 'https://github.com/johndoe',
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText(/mysite.com/)).toBeInTheDocument();
    expect(screen.getByText(/linkedin.com\/in\/johndoe/)).toBeInTheDocument();
    expect(screen.getByText(/github.com\/johndoe/)).toBeInTheDocument();
  });

  it('renders experience technologies', () => {
    const data: CVData = {
      ...mockData,
      experience: [
        {
          company: 'Tech Corp',
          position: 'Developer',
          startDate: '2020-01-01',
          technologies: ['React', 'Python'],
        },
      ],
    };
    render(<CVPreview data={data} />);
    expect(screen.getByText('React')).toBeInTheDocument();
    expect(screen.getByText('Python')).toBeInTheDocument();
  });
});
