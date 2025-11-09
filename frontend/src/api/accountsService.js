import api from './axios';

// Accounts API endpoints
const accountsService = {
  // Users
  getUsers: () => api.get('/accounts/users/'),
  getUser: (username) => api.get(`/accounts/users/${username}/`),
  createUser: (userData) => api.post('/accounts/users/', userData),
  updateUser: (username, userData) => api.put(`/accounts/users/${username}/`, userData),
  deleteUser: (username) => api.delete(`/accounts/users/${username}/`),

  // Students
  getStudents: () => api.get('/accounts/students/'),
  getStudent: (id) => api.get(`/accounts/students/${id}/`),
  createStudent: (studentData) => api.post('/accounts/students/', studentData),
  updateStudent: (id, studentData) => api.put(`/accounts/students/${id}/`, studentData),
  deleteStudent: (id) => api.delete(`/accounts/students/${id}/`),

  // Employees
  getEmployees: () => api.get('/accounts/employees/'),
  getEmployee: (id) => api.get(`/accounts/employees/${id}/`),
  createEmployee: (employeeData) => api.post('/accounts/employees/', employeeData),
  updateEmployee: (id, employeeData) => api.put(`/accounts/employees/${id}/`, employeeData),
  deleteEmployee: (id) => api.delete(`/accounts/employees/${id}/`),
};

export default accountsService;
