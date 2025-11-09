import api from './axios';

const fitnessService = {
  // ========== EXERCISES ==========
  
  /**
   * Get all exercises with optional filtering
   * @param {Object} params - {difficulty, type, created_by}
   */
  getExercises: (params) => api.get('/fitness/exercises/', { params }),
  
  /**
   * Get a specific exercise by ID
   * @param {string} id - MongoDB ObjectId
   */
  getExercise: (id) => api.get(`/fitness/exercises/${id}/`),
  
  /**
   * Create a new exercise
   * @param {Object} data - {name, type, description, duration, difficulty, video_url}
   */
  createExercise: (data) => api.post('/fitness/exercises/', data),
  
  /**
   * Update an existing exercise
   * @param {string} id - MongoDB ObjectId
   * @param {Object} data - Fields to update
   */
  updateExercise: (id, data) => api.put(`/fitness/exercises/${id}/`, data),
  
  /**
   * Delete an exercise
   * @param {string} id - MongoDB ObjectId
   */
  deleteExercise: (id) => api.delete(`/fitness/exercises/${id}/`),

  // ========== ROUTINES ==========
  
  /**
   * Get all routines with optional filtering
   * @param {Object} params - {user_id, is_template, created_by}
   */
  getRoutines: (params) => api.get('/fitness/routines/', { params }),
  
  /**
   * Get a specific routine by ID
   * @param {string} id - MongoDB ObjectId
   */
  getRoutine: (id) => api.get(`/fitness/routines/${id}/`),
  
  /**
   * Create a new routine
   * @param {Object} data - {name, description, exercises[], created_by, is_template, user_id}
   * exercises format: [{exercise_id, sets, reps, rest, duration}]
   */
  createRoutine: (data) => api.post('/fitness/routines/', data),
  
  /**
   * Update an existing routine
   * @param {string} id - MongoDB ObjectId
   * @param {Object} data - Fields to update
   */
  updateRoutine: (id, data) => api.put(`/fitness/routines/${id}/`, data),
  
  /**
   * Delete a routine
   * @param {string} id - MongoDB ObjectId
   */
  deleteRoutine: (id) => api.delete(`/fitness/routines/${id}/`),
  
  /**
   * Adopt a template routine for a user (create a copy)
   * @param {string} routineId - Template routine ID
   * @param {string} userId - User who's adopting the routine
   */
  adoptRoutine: (routineId, userId) => 
    api.post(`/fitness/routines/${routineId}/adopt/`, { user_id: userId }),

  // ========== PROGRESS ==========
  
  /**
   * Get all progress entries with optional filtering
   * @param {Object} params - {user_id, routine_id, exercise_id}
   */
  getProgress: (params) => api.get('/fitness/progress/', { params }),
  
  /**
   * Get a specific progress entry by ID
   * @param {string} id - MongoDB ObjectId
   */
  getProgressEntry: (id) => api.get(`/fitness/progress/${id}/`),
  
  /**
   * Create a new progress entry
   * @param {Object} data - {user_id, routine_id?, exercise_id?, date, repetitions, duration, effort_level, notes}
   */
  createProgress: (data) => api.post('/fitness/progress/', data),
  
  /**
   * Update an existing progress entry
   * @param {string} id - MongoDB ObjectId
   * @param {Object} data - Fields to update
   */
  updateProgress: (id, data) => api.put(`/fitness/progress/${id}/`, data),
  
  /**
   * Delete a progress entry
   * @param {string} id - MongoDB ObjectId
   */
  deleteProgress: (id) => api.delete(`/fitness/progress/${id}/`),

  // ========== RECOMMENDATIONS ==========
  
  /**
   * Get all recommendations with optional filtering
   * @param {Object} params - {user_id, trainer_id}
   */
  getRecommendations: (params) => api.get('/fitness/recommendations/', { params }),
  
  /**
   * Get a specific recommendation by ID
   * @param {string} id - MongoDB ObjectId
   */
  getRecommendation: (id) => api.get(`/fitness/recommendations/${id}/`),
  
  /**
   * Create a new recommendation
   * @param {Object} data - {trainer_id, user_id, message, related_progress_id?, related_routine_id?}
   */
  createRecommendation: (data) => api.post('/fitness/recommendations/', data),
  
  /**
   * Update an existing recommendation
   * @param {string} id - MongoDB ObjectId
   * @param {Object} data - Fields to update
   */
  updateRecommendation: (id, data) => api.put(`/fitness/recommendations/${id}/`, data),
  
  /**
   * Delete a recommendation
   * @param {string} id - MongoDB ObjectId
   */
  deleteRecommendation: (id) => api.delete(`/fitness/recommendations/${id}/`),

  // ========== FOLLOW-UPS ==========
  
  /**
   * Get all follow-ups with optional filtering
   * @param {Object} params - {user_id, trainer_id}
   */
  getFollowUps: (params) => api.get('/fitness/followups/', { params }),
  
  /**
   * Get a specific follow-up by ID
   * @param {string} id - MongoDB ObjectId
   */
  getFollowUp: (id) => api.get(`/fitness/followups/${id}/`),
  
  /**
   * Create a new follow-up
   * @param {Object} data - {trainer_id, user_id, progress_id?, comment}
   */
  createFollowUp: (data) => api.post('/fitness/followups/', data),
  
  /**
   * Update an existing follow-up
   * @param {string} id - MongoDB ObjectId
   * @param {Object} data - Fields to update
   */
  updateFollowUp: (id, data) => api.put(`/fitness/followups/${id}/`, data),
  
  /**
   * Delete a follow-up
   * @param {string} id - MongoDB ObjectId
   */
  deleteFollowUp: (id) => api.delete(`/fitness/followups/${id}/`),
};

export default fitnessService;
