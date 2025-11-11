# UniCali Fitness - Frontend

This is the React frontend for the UniCali Fitness tracking platform, integrated with the Django backend.

The original design is available at https://www.figma.com/design/Y9mOeDdeuX54YIqCPj79lH/Fitness-Tracking-Platform.

## Quick Start

### Prerequisites
- Node.js 16+ and npm
- Django backend running at `http://localhost:8000`

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

The app will run at `http://localhost:5173`

### Build for Production
```bash
npm run build
```

## Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Reusable UI components
│   ├── AdminDashboard.tsx
│   ├── ExerciseLibrary.tsx
│   ├── LoginPage.tsx
│   ├── PreDesignedRoutines.tsx
│   ├── ProgressView.tsx
│   ├── RoutinesView.tsx
│   ├── StatisticsView.tsx
│   ├── StudentDashboard.tsx
│   └── TrainerDashboard.tsx
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication state
├── hooks/             # Custom React hooks
│   └── useFitnessData.ts # Data fetching hooks
├── lib/               # Utilities and services
│   ├── api.ts         # API client
│   └── mock-data.ts   # Mock data (for reference)
├── types/             # TypeScript type definitions
│   └── index.ts
├── App.tsx            # Main app component
└── main.tsx           # App entry point
```

## API Integration

The frontend connects to the Django REST API. See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for detailed information about:

- API endpoints
- Data models
- How to update components to use the API
- Troubleshooting

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api
```

## Features

### For Students
- View and adopt pre-designed exercise routines
- Track workout progress
- View personal statistics and charts
- Receive recommendations from trainers

### For Instructors
- Create custom exercises
- Design workout routines
- Monitor student progress
- Provide personalized recommendations

### For Admins
- View system-wide statistics
- Manage users and instructors
- Monitor platform activity

## Development Status

### ✅ Completed
- API service layer (`src/lib/api.ts`)
- Custom React hooks (`src/hooks/useFitnessData.ts`)
- Authentication integration (`src/contexts/AuthContext.tsx`)
- Environment configuration
- Sample component integration (`ExerciseLibrary.tsx`)

### 🚧 In Progress
- Updating remaining components to use API instead of mock data
- See `INTEGRATION_GUIDE.md` for the list of components to update

## Technology Stack

- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **UI Components:** Custom components with Tailwind CSS
- **Charts:** Recharts
- **Icons:** Lucide React
- **State Management:** React Context API
- **HTTP Client:** Fetch API

## Contributing

When adding or modifying components:

1. Use the custom hooks from `src/hooks/useFitnessData.ts` for data fetching
2. Handle loading and error states
3. Use the API functions from `src/lib/api.ts` for mutations
4. Follow the TypeScript types defined in `src/types/index.ts`
5. Keep components focused and reusable

## Learn More

- [Integration Guide](./INTEGRATION_GUIDE.md) - Detailed API integration guide
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
