import axios from 'axios';
import { CVData } from '../types/cv.types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface CV {
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

interface Experience {
    company: string;
    position: string;
    start_date: string;
    end_date?: string;
    description?: string;
}

interface Education {
    institution: string;
    degree: string;
    start_date: string;
    end_date?: string;
}

interface Certificate {
    name: string;
    institution: string;
    date: string;
}

export class CVService {
    static async generateCV(data: CV): Promise<any> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/generate`, data);
            return response.data;
        } catch (error) {
            console.error('Error generating CV:', error);
            throw error;
        }
    }

    static async uploadPhoto(file: File): Promise<string> {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post(`${API_URL}/api/cv/upload-photo`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            return response.data.photo_url;
        } catch (error) {
            console.error('Error uploading photo:', error);
            throw error;
        }
    }

    static async exportCV(data: CV, format: 'pdf' | 'html' | 'md'): Promise<any> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/export`, data, {
                params: { format },
                responseType: 'blob',
            });

            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `cv.${format}`);
            document.body.appendChild(link);
            link.click();
            link.remove();

            return true;
        } catch (error) {
            console.error('Error exporting CV:', error);
            throw error;
        }
    }

    static async getTemplates(): Promise<string[]> {
        try {
            const response = await axios.get(`${API_URL}/api/cv/templates`);
            return response.data.templates;
        } catch (error) {
            console.error('Error getting templates:', error);
            throw error;
        }
    }

    static async generatePreview(data: CV, template: string): Promise<string> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/preview`, {
                ...data,
                template
            });
            return response.data.html;
        } catch (error) {
            console.error('Error generating preview:', error);
            throw error;
        }
    }
} 