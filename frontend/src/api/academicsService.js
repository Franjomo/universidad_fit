import api from './axios';

const academicsService = {
  // Programs
  getPrograms: (params) => api.get('/academics/programs/', { params }),
  getProgram: (code) => api.get(`/academics/programs/${code}/`),
  createProgram: (data) => api.post('/academics/programs/', data),
  updateProgram: (code, data) => api.put(`/academics/programs/${code}/`, data),
  deleteProgram: (code) => api.delete(`/academics/programs/${code}/`),

  // Subjects
  getSubjects: (params) => api.get('/academics/subjects/', { params }),
  getSubject: (code) => api.get(`/academics/subjects/${code}/`),
  createSubject: (data) => api.post('/academics/subjects/', data),
  updateSubject: (code, data) => api.put(`/academics/subjects/${code}/`, data),
  deleteSubject: (code) => api.delete(`/academics/subjects/${code}/`),

  // Groups
  getGroups: (params) => api.get('/academics/groups/', { params }),
  getGroup: (nrc) => api.get(`/academics/groups/${nrc}/`),
  createGroup: (data) => api.post('/academics/groups/', data),
  updateGroup: (nrc, data) => api.put(`/academics/groups/${nrc}/`, data),
  deleteGroup: (nrc) => api.delete(`/academics/groups/${nrc}/`),

  // Enrollments
  getEnrollments: (params) => api.get('/academics/enrollments/', { params }),
  getEnrollment: (id) => api.get(`/academics/enrollments/${id}/`),
  createEnrollment: (data) => api.post('/academics/enrollments/', data),
  updateEnrollment: (id, data) => api.put(`/academics/enrollments/${id}/`, data),
  deleteEnrollment: (id) => api.delete(`/academics/enrollments/${id}/`),
};

export default academicsService;
