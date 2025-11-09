import api from './axios';

const humanResourcesService = {
  // Contract Types
  getContractTypes: () => api.get('/hr/contract-types/'),
  getContractType: (name) => api.get(`/hr/contract-types/${name}/`),
  createContractType: (data) => api.post('/hr/contract-types/', data),
  updateContractType: (name, data) => api.put(`/hr/contract-types/${name}/`, data),
  deleteContractType: (name) => api.delete(`/hr/contract-types/${name}/`),

  // Employee Types
  getEmployeeTypes: () => api.get('/hr/employee-types/'),
  getEmployeeType: (name) => api.get(`/hr/employee-types/${name}/`),
  createEmployeeType: (data) => api.post('/hr/employee-types/', data),
  updateEmployeeType: (name, data) => api.put(`/hr/employee-types/${name}/`, data),
  deleteEmployeeType: (name) => api.delete(`/hr/employee-types/${name}/`),
};

export default humanResourcesService;
