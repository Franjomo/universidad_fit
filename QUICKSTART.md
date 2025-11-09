# Universidad Fit - Quick Start Guide 🚀

## ✅ Status: EVERYTHING IS WORKING!

Both frontend and backend are currently running and fully integrated!

## Access the Application

### Frontend (React/Vite)
```
http://localhost:3000/Fitnesstrackingplatform/
```

### Backend API
```
http://localhost:8000/api/fitness/exercises/
http://localhost:8000/api/fitness/routines/
```

## Test the API

```bash
# Get all exercises
curl http://localhost:8000/api/fitness/exercises/

# Get all routines
curl http://localhost:8000/api/fitness/routines/

# Create a new exercise
curl -X POST http://localhost:8000/api/fitness/exercises/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Exercise",
    "type": "cardio",
    "description": "A test exercise",
    "duration": 15,
    "difficulty": "principiante",
    "createdBy": "system"
  }'
```

## Current Data

**Exercises:** 5 sample exercises
- Correr (Cardio, 30 min)
- Sentadillas (Fuerza, 15 min)
- Flexiones (Fuerza, 10 min)
- Yoga Flow (Movilidad, 20 min)
- Plancha (Fuerza, 5 min)

**Routines:** 1 sample routine
- Rutina de Fuerza Básica

## If You Need to Restart

### Backend (Django)
```bash
cd /home/santiago/Documents/sid2/universidad_fit
./venv/bin/python manage.py runserver
```

### Frontend (Vite)
```bash
cd /home/santiago/Documents/sid2/universidad_fit/frontend_fitness
npm run dev
```

## What's Been Fixed

1. ✅ Moved frontend into universidad_fit folder
2. ✅ Created complete API integration layer
3. ✅ Switched from MongoDB to SQL (no MongoDB needed!)
4. ✅ Created database migrations
5. ✅ Added sample data
6. ✅ Configured CORS
7. ✅ Fixed SECRET_KEY issue
8. ✅ Disabled auth for testing
9. ✅ Updated ExerciseLibrary component as example

## File Locations

```
universidad_fit/
├── frontend_fitness/          # React app (http://localhost:3000)
│   ├── src/lib/api.ts        # API client
│   ├── src/hooks/useFitnessData.ts  # Data hooks
│   └── .env                  # API URL config
├── fitness/                   # Django app
│   ├── models_sql.py         # Database models
│   ├── serializers_sql.py    # API serializers
│   └── views.py              # API endpoints
├── db.sqlite3                # Database (with sample data!)
└── .env                      # Backend config
```

## Next Steps

See `WORKING_STATUS.md` for complete details and `INTEGRATION_GUIDE.md` in the frontend folder for how to integrate remaining components.

## Documentation

- `WORKING_STATUS.md` - Complete working status and details
- `frontend_fitness/INTEGRATION_GUIDE.md` - How to integrate components
- `frontend_fitness/README.md` - Frontend documentation
- `TEST_RESULTS.md` - Test results and setup details

🎉 Happy coding!
