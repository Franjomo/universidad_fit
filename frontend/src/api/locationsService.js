import api from './axios';

const locationsService = {
  // Countries
  getCountries: () => api.get('/locations/countries/'),
  getCountry: (code) => api.get(`/locations/countries/${code}/`),
  createCountry: (data) => api.post('/locations/countries/', data),
  updateCountry: (code, data) => api.put(`/locations/countries/${code}/`, data),
  deleteCountry: (code) => api.delete(`/locations/countries/${code}/`),

  // Departments
  getDepartments: (params) => api.get('/locations/departments/', { params }),
  getDepartment: (code) => api.get(`/locations/departments/${code}/`),
  createDepartment: (data) => api.post('/locations/departments/', data),
  updateDepartment: (code, data) => api.put(`/locations/departments/${code}/`, data),
  deleteDepartment: (code) => api.delete(`/locations/departments/${code}/`),

  // Cities
  getCities: (params) => api.get('/locations/cities/', { params }),
  getCity: (code) => api.get(`/locations/cities/${code}/`),
  createCity: (data) => api.post('/locations/cities/', data),
  updateCity: (code, data) => api.put(`/locations/cities/${code}/`, data),
  deleteCity: (code) => api.delete(`/locations/cities/${code}/`),

  // Campuses
  getCampuses: (params) => api.get('/locations/campuses/', { params }),
  getCampus: (code) => api.get(`/locations/campuses/${code}/`),
  createCampus: (data) => api.post('/locations/campuses/', data),
  updateCampus: (code, data) => api.put(`/locations/campuses/${code}/`, data),
  deleteCampus: (code) => api.delete(`/locations/campuses/${code}/`),

  // Faculties
  getFaculties: () => api.get('/locations/faculties/'),
  getFaculty: (code) => api.get(`/locations/faculties/${code}/`),
  createFaculty: (data) => api.post('/locations/faculties/', data),
  updateFaculty: (code, data) => api.put(`/locations/faculties/${code}/`, data),
  deleteFaculty: (code) => api.delete(`/locations/faculties/${code}/`),

  // Areas
  getAreas: (params) => api.get('/locations/areas/', { params }),
  getArea: (code) => api.get(`/locations/areas/${code}/`),
  createArea: (data) => api.post('/locations/areas/', data),
  updateArea: (code, data) => api.put(`/locations/areas/${code}/`, data),
  deleteArea: (code) => api.delete(`/locations/areas/${code}/`),
};

export default locationsService;
