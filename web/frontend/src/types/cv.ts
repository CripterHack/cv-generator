export interface Education {
  institution: string;
  degree: string;
  fieldOfStudy: string;
  startDate: string;
  endDate?: string;
  description?: string;
  location?: string;
  achievements?: string[];
}

export interface Experience {
  company: string;
  position: string;
  startDate: string;
  endDate?: string;
  description?: string;
  location?: string;
  achievements?: string[];
  technologies?: string[];
}

export interface Skill {
  name: string;
  level?: number;
  category?: string;
  yearsOfExperience?: number;
}

export interface Certificate {
  name: string;
  issuer: string;
  dateObtained: string;
  expiryDate?: string;
  credentialId?: string;
  credentialUrl?: string;
}

export interface Language {
  name: string;
  level: string;
  certification?: string;
}

export interface CVData {
  fullName: string;
  email: string;
  phone?: string;
  summary?: string;
  education: Education[];
  experience: Experience[];
  skills: Skill[];
  certificates: Certificate[];
  languages: Language[];
  website?: string;
  linkedin?: string;
  github?: string;
  photoUrl?: string;
}

export type CVDataApi = {
  full_name: string;
  email: string;
  phone?: string;
  summary?: string;
  education: {
    institution: string;
    degree: string;
    field_of_study: string;
    start_date: string;
    end_date?: string;
    description?: string;
    location?: string;
    achievements?: string[];
  }[];
  experience: {
    company: string;
    position: string;
    start_date: string;
    end_date?: string;
    description?: string;
    location?: string;
    achievements?: string[];
    technologies?: string[];
  }[];
  skills: {
    name: string;
    level?: number;
    category?: string;
    years_of_experience?: number;
  }[];
  certificates: {
    name: string;
    issuer: string;
    date_obtained: string;
    expiry_date?: string;
    credential_id?: string;
    credential_url?: string;
  }[];
  languages: {
    name: string;
    level: string;
    certification?: string;
  }[];
  website?: string;
  linkedin?: string;
  github?: string;
  photo_url?: string;
};

function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

function transformValue(val: unknown): unknown {
  if (Array.isArray(val)) {
    return val.map((item) =>
      item && typeof item === 'object' ? transformKeysToSnake(item as Record<string, unknown>) : item,
    );
  }
  return val;
}

function transformKeysToSnake(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    result[toSnakeCase(key)] = transformValue(value);
  }
  return result;
}

export function toApiFormat(data: CVData): CVDataApi {
  return transformKeysToSnake(data as unknown as Record<string, unknown>) as unknown as CVDataApi;
}