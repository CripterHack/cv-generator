import axios from 'axios';
import { CVService } from '../CVService';
import { CVData } from '../../types/cv';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

beforeAll(() => {
  global.URL.createObjectURL = jest.fn(() => 'blob:mock-url');
  global.URL.revokeObjectURL = jest.fn();
});

describe('CVService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const sampleCV: CVData = {
    fullName: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    summary: 'Experienced software engineer',
    experience: [
      {
        company: 'Tech Corp',
        position: 'Senior Developer',
        startDate: '2020-01-01',
        endDate: '2023-12-31',
        description: 'Development of web applications',
      },
    ],
    education: [],
    skills: [{ name: 'Python', level: 5 }],
    certificates: [],
    languages: [],
  };

  describe('generateCV', () => {
    it('should send transformed snake_case data to API', async () => {
      const expectedResponse = { message: 'CV generado exitosamente', data: {} };
      mockedAxios.post.mockResolvedValueOnce({ data: expectedResponse });

      const result = await CVService.generateCV(sampleCV);
      expect(result).toEqual(expectedResponse);

      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/cv/generate'),
        expect.objectContaining({
          full_name: 'John Doe',
          email: 'john@example.com',
          experience: [
            expect.objectContaining({
              company: 'Tech Corp',
              start_date: '2020-01-01',
            }),
          ],
          skills: [
            expect.objectContaining({
              name: 'Python',
              level: 5,
            }),
          ],
        }),
      );
    });

    it('should handle errors', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('API Error'));
      await expect(CVService.generateCV(sampleCV)).rejects.toThrow('API Error');
    });
  });

  describe('createCV', () => {
    it('should create CV with transformed data', async () => {
      const expectedResponse = { full_name: 'John Doe', email: 'john@example.com' };
      mockedAxios.post.mockResolvedValueOnce({ data: expectedResponse });

      const result = await CVService.createCV(sampleCV);
      expect(result).toEqual(expectedResponse);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/cv/'),
        expect.objectContaining({
          full_name: 'John Doe',
          email: 'john@example.com',
        }),
      );
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
        expect.any(Object),
      );
    });

    it('should handle upload errors', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Upload Error'));
      const file = new File([''], 'photo.jpg', { type: 'image/jpeg' });
      await expect(CVService.uploadPhoto(file)).rejects.toThrow('Upload Error');
    });
  });

  describe('exportCV', () => {
    it('should send transformed data and format param', async () => {
      const blob = new Blob(['PDF content'], { type: 'application/pdf' });
      mockedAxios.post.mockResolvedValueOnce({ data: blob });

      const result = await CVService.exportCV(sampleCV, 'pdf');
      expect(result).toBe(true);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/cv/export'),
        expect.objectContaining({
          full_name: 'John Doe',
          email: 'john@example.com',
        }),
        expect.objectContaining({
          params: { format: 'pdf' },
          responseType: 'blob',
        }),
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
        expect.stringContaining('/api/cv/templates'),
      );
    });

    it('should handle template fetch errors', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Template Error'));
      await expect(CVService.getTemplates()).rejects.toThrow('Template Error');
    });
  });
});
