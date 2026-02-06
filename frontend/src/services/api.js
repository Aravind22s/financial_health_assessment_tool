import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Companies
export const getCompanies = () => api.get('/companies/');
export const getCompany = (id) => api.get(`/companies/${id}/`);
export const createCompany = (data) => api.post('/companies/', data);
export const updateCompany = (id, data) => api.put(`/companies/${id}/`, data);

// Financial Data
export const uploadFinancialData = (formData) => {
  return api.post('/financial-data/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
export const processFinancialData = (id) => api.post(`/financial-data/${id}/process/`);
export const getFinancialData = (companyId) => api.get(`/financial-data/?company=${companyId}`);

// Metrics
export const getMetrics = (companyId) => api.get(`/metrics/?company=${companyId}`);
export const getLatestMetrics = (companyId) => api.get(`/metrics/latest/?company=${companyId}`);

// Credit Assessment
export const assessCredit = (companyId) => api.post('/credit-assessments/assess/', { company_id: companyId });
export const getCreditAssessments = (companyId) => api.get(`/credit-assessments/?company=${companyId}`);

// Recommendations
export const generateRecommendations = (companyId, language = 'en') => 
  api.post('/recommendations/generate/', { company_id: companyId, language });
export const getRecommendations = (companyId) => api.get(`/recommendations/?company=${companyId}`);

// Forecasts
export const generateForecast = (companyId, months = 12) => 
  api.post('/forecasts/generate/', { company_id: companyId, months });
export const getForecasts = (companyId) => api.get(`/forecasts/?company=${companyId}`);

// Reports
export const generateReport = (companyId, reportType = 'comprehensive', language = 'en') => 
  api.post('/reports/generate/', { company_id: companyId, report_type: reportType, language });
export const getReports = (companyId) => api.get(`/reports/?company=${companyId}`);

// Benchmarks
export const getBenchmark = (industry) => api.get(`/benchmarks/by_industry/?industry=${industry}`);

export default api;
