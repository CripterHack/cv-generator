export interface CVData {
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

export interface Experience {
  company: string;
  position: string;
  start_date: string;
  end_date?: string;
  description?: string;
}

export interface Education {
  institution: string;
  degree: string;
  start_date: string;
  end_date?: string;
}

export interface Certificate {
  name: string;
  institution: string;
  date: string;
}

export interface PreviewProps {
  data: CVData;
  template: string;
} 