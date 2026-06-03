import axios from 'axios';
import { CVService } from '../CVService';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('CVService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const sampleCV = {
    name: 'John Doe',
    title: 'Software Engineer',
    phone: '+1234567890',
    age: 30,
    city: 'New York',
    summary: 'Experienced software engineer',
    show_photo: false,
    professional_experience: [],
    academic_experience: [],
    skills: [],
    certificates: []
  };

  describe('generateCV', () => {
    it('should successfully generate CV', async () => {
      const expectedResponse = { html: '<div>CV Content</div>' };
      mockedAxios.post.mockResolvedValueOnce({ data: expectedResponse });

      const result = await CVService.generateCV(sampleCV);
      expect(result).toEqual(expectedResponse);
        expect(mockedAxios.post).toHaveBeenCalledWith(
          expect.stringContaining('/api/cv/generate'),
          sampleCV
        );
    });

    it('should handle errors', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('API Error'));
      await expect(CVService.generateCV(sampleCV)).rejects.toThrow('API Error');
    });
  });

  describe('uploadPhoto', () => {
    it('should successfully upload photo', async () => {
      const expectedResponse = { photo_url: 'http://example.com/photo.jpg' };
      mockedAxios.post.mockResolvedValueOnce({ data: expectedResponse });

      const file = new File([''], 'photo.jpg', { type: 'image/jpeg' });
      const result = await CVService.uploadPhoto(file);
      
      expect(result).toBe(expectedResponse.photo_url);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/cv/upload-photo'),
        expect.any(FormData),
        expect.any(Object)
      );
    });

    it('should handle upload errors', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Upload Error'));
      const file = new File([''], 'photo.jpg', { type: 'image/jpeg' });
      await expect(CVService.uploadPhoto(file)).rejects.toThrow('Upload Error');
    });
  });

  describe('exportCV', () => {
    it('should successfully export CV as PDF', async () => {
      const blob = new Blob(['PDF content'], { type: 'application/pdf' });
      mockedAxios.post.mockResolvedValueOnce({ data: blob });

      const result = await CVService.exportCV(sampleCV, 'pdf');
      expect(result).toBe(true);
        expect(mockedAxios.post).toHaveBeenCalledWith(
          expect.stringContaining('/api/cv/export'),
          sampleCV,
        expect.objectContaining({
          params: { format: 'pdf' },
          responseType: 'blob'
        })
      );
    });

    it('should handle export errors', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Export Error'));
      await expect(CVService.exportCV(sampleCV, 'pdf')).rejects.toThrow('Export Error');
    });
  });

  describe('getTemplates', () => {
    it('should successfully get templates', async () => {
      const expectedTemplates = ['template1.html', 'template2.html'];
      mockedAxios.get.mockResolvedValueOnce({ data: { templates: expectedTemplates } });

      const result = await CVService.getTemplates();
      expect(result).toEqual(expectedTemplates);
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/cv/templates')
      );
    });

    it('should handle template fetch errors', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Template Error'));
      await expect(CVService.getTemplates()).rejects.toThrow('Template Error');
    });
  });
}); 