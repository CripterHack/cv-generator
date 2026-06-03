import axios from 'axios';
import { CVData, toApiFormat } from '../types/cv';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export class CVService {
    static async createCV(data: CVData): Promise<any> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/`, toApiFormat(data));
            return response.data;
        } catch (error) {
            console.error('Error creating CV:', error);
            throw error;
        }
    }

    static async getCV(email: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/api/cv/${encodeURIComponent(email)}`);
            return response.data;
        } catch (error) {
            console.error('Error getting CV:', error);
            throw error;
        }
    }

    static async updateCV(email: string, data: CVData): Promise<any> {
        try {
            const response = await axios.put(
                `${API_URL}/api/cv/${encodeURIComponent(email)}`,
                toApiFormat(data),
            );
            return response.data;
        } catch (error) {
            console.error('Error updating CV:', error);
            throw error;
        }
    }

    static async generateCV(data: CVData): Promise<any> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/generate`, toApiFormat(data));
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

    static async exportCV(data: CVData, format: 'pdf' | 'html' | 'md'): Promise<any> {
        try {
            const response = await axios.post(`${API_URL}/api/cv/export`, toApiFormat(data), {
                params: { format },
                responseType: 'blob',
            });

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
}
