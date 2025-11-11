import { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/LoginPage';
import { DashboardLayout } from './components/DashboardLayout';
import { StudentDashboard } from './components/StudentDashboard';
import { ExerciseLibrary } from './components/ExerciseLibrary';
import { RoutinesView } from './components/RoutinesView';
import { ProgressView } from './components/ProgressView';
import { TrainerDashboard } from './components/TrainerDashboard';
import { PreDesignedRoutines } from './components/PreDesignedRoutines';
import { AdminDashboard } from './components/AdminDashboard';
import { StatisticsView } from './components/StatisticsView';
import { SettingsView } from './components/SettingsView';
import { Toaster } from './components/ui/sonner';

function AppContent() {
  const { currentUser } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  if (!currentUser) {
    return <LoginPage />;
  }

  const renderContent = () => {
    // Student/Employee views
    if (currentUser.role === 'student' || currentUser.role === 'employee') {
      switch (activeTab) {
        case 'dashboard':
          return <StudentDashboard />;
        case 'routines':
          return <RoutinesView />;
        case 'exercises':
          return <ExerciseLibrary />;
        case 'progress':
          return <ProgressView />;
        default:
          return <StudentDashboard />;
      }
    }

    // Instructor views
    if (currentUser.role === 'instructor') {
      switch (activeTab) {
        case 'dashboard':
          return <TrainerDashboard />;
        case 'my-users':
          return <TrainerDashboard />;
        case 'pre-designed':
          return <PreDesignedRoutines />;
        case 'exercises':
          return <ExerciseLibrary />;
        default:
          return <TrainerDashboard />;
      }
    }

    // Admin views
    if (currentUser.role === 'admin') {
      switch (activeTab) {
        case 'dashboard':
          return <AdminDashboard />;
        case 'assignments':
          return <AdminDashboard />;
        case 'statistics':
          return <StatisticsView />;
        case 'settings':
          return <SettingsView />;
        default:
          return <AdminDashboard />;
      }
    }

    return <StudentDashboard />;
  };

  return (
    <DashboardLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {renderContent()}
    </DashboardLayout>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
      <Toaster />
    </AuthProvider>
  );
}
