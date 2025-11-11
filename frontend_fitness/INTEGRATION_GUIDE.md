# Frontend-Backend Integration Guide

This document explains how the frontend has been integrated with the Django backend.

## What Has Been Done

### 1. ✅ Folder Structure
- Moved `Fitnesstrackingplatform` → `universidad_fit/frontend_fitness`
- Frontend is now located inside the Django project directory

### 2. ✅ API Service Layer Created
**File:** `src/lib/api.ts`

This file contains all API calls organized by resource:
- `authAPI` - Authentication (login, logout, getCurrentUser)
- `exercisesAPI` - Exercise CRUD operations
- `routinesAPI` - Routine CRUD operations + adopt functionality
- `progressAPI` - Progress log CRUD operations
- `recommendationsAPI` - Recommendation CRUD operations
- `followUpsAPI` - Follow-up CRUD operations

### 3. ✅ Custom React Hooks Created
**File:** `src/hooks/useFitnessData.ts`

Provides easy-to-use hooks for data fetching:
- `useExercises()` - Fetch and manage exercises
- `useRoutines()` - Fetch and manage routines
- `useProgress()` - Fetch and manage progress logs
- `useRecommendations()` - Fetch and manage recommendations

### 4. ✅ Authentication Updated
**File:** `src/contexts/AuthContext.tsx`

- Now uses real backend authentication
- Stores JWT token in localStorage
- Auto-restores session on page reload
- Login/logout methods are now async

### 5. ✅ Environment Variables Configured
**Files:** `.env` and `.env.example`

```env
VITE_API_URL=http://localhost:8000/api
```

### 6. ✅ Component Updated (Example)
**File:** `src/components/ExerciseLibrary.tsx`

- Replaced `mockExercises` with `useExercises()` hook
- Added loading and error states
- Updated `handleAddExercise` to use `exercisesAPI.create()`

## Components Still Using Mock Data

The following components need to be updated to use the API:

1. **ProgressView.tsx** - Uses `mockProgressLogs`, `mockRoutines`, `mockExercises`
2. **PreDesignedRoutines.tsx** - Uses `mockRoutines`, `mockExercises`
3. **RoutinesView.tsx** - Uses `mockRoutines`, `mockExercises`
4. **StatisticsView.tsx** - Uses `mockUserStatistics`
5. **StudentDashboard.tsx** - Uses multiple mock data sources
6. **TrainerDashboard.tsx** - Uses `mockUsers`, `mockRecommendations`, etc.
7. **AdminDashboard.tsx** - Uses `mockUsers`, `mockInstructorStatistics`, etc.

## How to Update a Component

Follow this pattern for each component:

### Step 1: Replace imports
```typescript
// OLD:
import { mockExercises, mockRoutines } from '../lib/mock-data';

// NEW:
import { useExercises, useRoutines } from '../hooks/useFitnessData';
import { exercisesAPI, routinesAPI } from '../lib/api';
```

### Step 2: Replace useState with hooks
```typescript
// OLD:
const [exercises, setExercises] = useState(mockExercises);

// NEW:
const { exercises, loading, error, refetch } = useExercises();
```

### Step 3: Add loading/error states
```typescript
if (loading) {
  return <div>Cargando...</div>;
}

if (error) {
  return <div>Error: {error}</div>;
}
```

### Step 4: Update CRUD operations
```typescript
// OLD:
const handleAddExercise = () => {
  setExercises([...exercises, newExercise]);
};

// NEW:
const handleAddExercise = async () => {
  try {
    await exercisesAPI.create(newExercise);
    await refetch(); // Refresh the list
  } catch (error) {
    console.error('Failed to create exercise:', error);
  }
};
```

## Backend API Endpoints

### Authentication
- `POST /api/accounts/login/` - Login
- `POST /api/accounts/logout/` - Logout
- `GET /api/accounts/me/` - Get current user

### Exercises
- `GET /api/fitness/exercises/` - List exercises (supports filters: difficulty, type, created_by)
- `POST /api/fitness/exercises/` - Create exercise
- `GET /api/fitness/exercises/{id}/` - Get exercise
- `PUT /api/fitness/exercises/{id}/` - Update exercise
- `DELETE /api/fitness/exercises/{id}/` - Delete exercise

### Routines
- `GET /api/fitness/routines/` - List routines (supports filters: user_id, is_template, created_by)
- `POST /api/fitness/routines/` - Create routine
- `GET /api/fitness/routines/{id}/` - Get routine
- `PUT /api/fitness/routines/{id}/` - Update routine
- `DELETE /api/fitness/routines/{id}/` - Delete routine
- `POST /api/fitness/routines/{id}/adopt/` - Adopt a template routine

### Progress
- `GET /api/fitness/progress/` - List progress logs (supports filters: user_id, routine_id, exercise_id)
- `POST /api/fitness/progress/` - Create progress log
- `GET /api/fitness/progress/{id}/` - Get progress log
- `PUT /api/fitness/progress/{id}/` - Update progress log
- `DELETE /api/fitness/progress/{id}/` - Delete progress log

### Recommendations
- `GET /api/fitness/recommendations/` - List recommendations (supports filters: user_id, trainer_id)
- `POST /api/fitness/recommendations/` - Create recommendation
- `GET /api/fitness/recommendations/{id}/` - Get recommendation
- `PUT /api/fitness/recommendations/{id}/` - Update recommendation
- `DELETE /api/fitness/recommendations/{id}/` - Delete recommendation

### Follow-ups
- `GET /api/fitness/followups/` - List follow-ups (supports filters: user_id, trainer_id)
- `POST /api/fitness/followups/` - Create follow-up
- `GET /api/fitness/followups/{id}/` - Get follow-up
- `PUT /api/fitness/followups/{id}/` - Update follow-up
- `DELETE /api/fitness/followups/{id}/` - Delete follow-up

## Data Model Mappings

### Frontend → Backend Field Name Differences

The backend uses snake_case while frontend uses camelCase. The API layer handles this conversion automatically in most cases, but be aware:

| Frontend | Backend |
|----------|---------|
| `createdBy` | `created_by` |
| `createdAt` | `created_at` |
| `userId` | `user_id` |
| `exerciseId` | `exercise_id` |
| `routineId` | `routine_id` |
| `videoUrl` | `video_url` |
| `effortLevel` | `effort_level` |
| `isTemplate` | `is_template` |

### Difficulty Levels
| Frontend | Backend |
|----------|---------|
| `principiante` | `baja` |
| `intermedio` | `media` |
| `avanzado` | `alta` |

**Note:** You may need to add a mapping function to convert between these values.

## Running the Application

### Backend (Django)
```bash
cd universidad_fit
python manage.py runserver
```

### Frontend (Vite + React)
```bash
cd universidad_fit/frontend_fitness
npm install
npm run dev
```

The frontend will run on `http://localhost:5173` and connect to the backend at `http://localhost:8000`.

## CORS Configuration

Make sure the Django backend has CORS configured to allow requests from the frontend:

**File:** `universidad_fit/universidad_fit/settings.py`

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]
CORS_ALLOW_CREDENTIALS = True
```

## Next Steps

1. ✅ Update remaining components to use API hooks
2. ✅ Test all CRUD operations
3. ✅ Add proper error handling and user feedback
4. ✅ Implement loading spinners for better UX
5. ✅ Test authentication flow end-to-end
6. ✅ Add field name conversion utilities if needed for difficulty levels
7. ✅ Test with real backend data

## Troubleshooting

### CORS Errors
- Check that Django CORS settings include the frontend URL
- Verify `CORS_ALLOW_CREDENTIALS = True` is set

### 401 Unauthorized
- Check that the token is being sent in the Authorization header
- Verify the user is logged in
- Check token expiration

### Field Name Mismatches
- Check the API response in browser DevTools
- Add conversion utilities in `src/lib/api.ts` if needed
- Ensure serializers match frontend expectations

### Cannot Connect to Backend
- Verify backend is running on `http://localhost:8000`
- Check `.env` file has correct `VITE_API_URL`
- Restart the Vite dev server after changing `.env`
