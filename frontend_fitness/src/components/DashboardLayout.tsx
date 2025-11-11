import { ReactNode } from 'react';
import { Button } from './ui/button';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Dumbbell, LogOut, Home, Dumbbell as DumbbellIcon, BarChart3, Users, Settings } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';

interface DashboardLayoutProps {
  children: ReactNode;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function DashboardLayout({ children, activeTab, onTabChange }: DashboardLayoutProps) {
  const { currentUser, logout } = useAuth();

  if (!currentUser) return null;

  const getInitials = () => {
    return `${currentUser.firstName[0]}${currentUser.lastName[0]}`.toUpperCase();
  };

  const getRoleName = () => {
    switch (currentUser.role) {
      case 'student': return 'Estudiante';
      case 'employee': return 'Colaborador';
      case 'instructor': return 'Entrenador';
      case 'admin': return 'Administrador';
      default: return '';
    }
  };

  const navigationItems = [
    { id: 'dashboard', label: 'Inicio', icon: Home },
    { id: 'routines', label: 'Mis Rutinas', icon: DumbbellIcon },
    { id: 'exercises', label: 'Ejercicios', icon: Dumbbell },
    { id: 'progress', label: 'Mi Progreso', icon: BarChart3 },
  ];

  const trainerNavigationItems = [
    { id: 'dashboard', label: 'Inicio', icon: Home },
    { id: 'my-users', label: 'Mis Usuarios', icon: Users },
    { id: 'pre-designed', label: 'Rutinas Prediseñadas', icon: DumbbellIcon },
    { id: 'exercises', label: 'Ejercicios', icon: Dumbbell },
  ];

  const adminNavigationItems = [
    { id: 'dashboard', label: 'Inicio', icon: Home },
    { id: 'assignments', label: 'Asignaciones', icon: Users },
    { id: 'statistics', label: 'Estadísticas', icon: BarChart3 },
    { id: 'settings', label: 'Configuración', icon: Settings },
  ];

  const getNavigationItems = () => {
    if (currentUser.role === 'instructor') return trainerNavigationItems;
    if (currentUser.role === 'admin') return adminNavigationItems;
    return navigationItems;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Dumbbell className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-blue-900">UniCali Fitness</h3>
                <p className="text-xs text-gray-600">{getRoleName()}</p>
              </div>
            </div>

            {/* User Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                  <Avatar>
                    <AvatarFallback>{getInitials()}</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end">
                <DropdownMenuLabel>
                  <div>
                    <p>{currentUser.firstName} {currentUser.lastName}</p>
                    <p className="text-xs text-gray-600">{currentUser.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={logout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Cerrar sesión</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-1 overflow-x-auto">
            {getNavigationItems().map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => onTabChange(item.id)}
                  className={`
                    flex items-center gap-2 px-4 py-3 border-b-2 transition-colors whitespace-nowrap
                    ${activeTab === item.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
