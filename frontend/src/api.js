import axios from 'axios';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getHealth = () => api.get('/health');
export const register = (data) => api.post('/register', data);
export const login = (data) => api.post('/login', data);
export const analyzeSuitability = (data) => api.post('/analyze-suitability', data);
export const generateReport = (data) => api.post('/generate-report', data, { responseType: 'blob' });
export const getMyReports = () => api.get('/my-reports');

export default api;
