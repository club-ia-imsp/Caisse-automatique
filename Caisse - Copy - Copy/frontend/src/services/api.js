import axios from 'axios';

// With Vite proxy, API calls go through localhost:3000 → proxied to :8000
const API_URL = '';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('automaticcheck_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor for 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('automaticcheck_token');
      localStorage.removeItem('automaticcheck_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = (credentials) => api.post('/auth/login', credentials);
export const getMe = () => api.get('/auth/me');

// Products
export const getProducts = (skip = 0, limit = 50) => api.get(`/products/?skip=${skip}&limit=${limit}`);
export const getProduct = (id) => api.get(`/products/${id}`);
export const createProduct = (data) => api.post('/products/', data);
export const updateProduct = (id, data) => api.put(`/products/${id}`, data);
export const deleteProduct = (id) => api.delete(`/products/${id}`);
export const trainProduct = (id, formData) =>
  api.post(`/products/${id}/train`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
export const getProductEmbeddings = (id) => api.get(`/products/${id}/embeddings`);

// Invoices
export const getInvoices = (skip = 0, limit = 50) => api.get(`/invoices/?skip=${skip}&limit=${limit}`);
export const getInvoice = (id) => api.get(`/invoices/${id}`);
export const createInvoice = (data) => api.post('/invoices/', data);
export const updatePayment = (id, data) => api.patch(`/invoices/${id}/payment`, data);
export const getInvoicePdf = (id) => `/api/invoices/${id}/pdf`;

// Health
export const healthCheck = () => api.get('/health');

// WebSocket URL - connects through Vite proxy to backend
export const getWsUrl = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host; // localhost:3000 → proxied to ws://localhost:8000
  return `${protocol}//${host}/ws/detection`;
};

export default api;
