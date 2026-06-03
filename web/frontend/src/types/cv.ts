export interface Education {
  institution: string;
  degree: string;
  fieldOfStudy: string;
  startDate: string;
  endDate?: string;
  description?: string;
}

export interface Experience {
  company: string;
  position: string;
  startDate: string;
  endDate?: string;
  description?: string;
}

export interface Skill {
  name: string;
  level?: number;
}

export interface CVData {
  fullName: string;
  email: string;
  phone?: string;
  summary?: string;
  education: Education[];
  experience: Experience[];
  skills: Skill[];
} 