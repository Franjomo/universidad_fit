import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import type { User, UserRole } from '../types';
import { authAPI } from '../lib/api';

interface AuthContextType {
  currentUser: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in on mount
  useEffect(() => {
    const initAuth = async () => {
      const authData = localStorage.getItem('auth');
      if (authData) {
        try {
          const parsed = JSON.parse(authData);
          if (parsed.user) {
            // Use stored user if available
            setCurrentUser(parsed.user);
          } else {
            // Try to get current user from API
            const user = await authAPI.getCurrentUser();
            // Transform backend format to frontend format
            const frontendUser: User = {
              id: user.username || user.student || user.employee || '',
              email: user.student_details?.email || user.employee_details?.email || '',
              firstName: user.student_details?.first_name || user.employee_details?.first_name || '',
              lastName: user.student_details?.last_name || user.employee_details?.last_name || '',
              role: user.role?.toLowerCase() as UserRole || 'student',
              programId: user.student_details?.program_id,
              departmentId: user.employee_details?.faculty,
            };
            setCurrentUser(frontendUser);
          }
        } catch (error) {
          console.error('Failed to restore session:', error);
          localStorage.removeItem('auth');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authAPI.login(email, password);
      // Transform backend user format to frontend format
      const backendUser = response.user;
      // Map backend roles to frontend roles
      let frontendRole: UserRole = 'student';
      if (backendUser.role === 'STUDENT') {
        frontendRole = 'student';
      } else if (backendUser.role === 'EMPLOYEE') {
        // Check if employee is a trainer/instructor
        if (backendUser.employee_details?.employee_type === 'Entrenador') {
          frontendRole = 'instructor';
        } else {
          frontendRole = 'employee';
        }
      } else if (backendUser.role === 'ADMIN') {
        frontendRole = 'admin';
      }
      
      const frontendUser: User = {
        id: backendUser.username || backendUser.student || backendUser.employee || '',
        email: backendUser.student_details?.email || backendUser.employee_details?.email || email,
        firstName: backendUser.student_details?.first_name || backendUser.employee_details?.first_name || '',
        lastName: backendUser.student_details?.last_name || backendUser.employee_details?.last_name || '',
        role: frontendRole,
        programId: backendUser.student_details?.program_id,
        departmentId: backendUser.employee_details?.faculty,
      };
      setCurrentUser(frontendUser);
      localStorage.setItem('auth', JSON.stringify({ token: response.token, user: frontendUser }));
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setCurrentUser(null);
      localStorage.removeItem('auth');
    }
  };

  return (
    <AuthContext.Provider value={{ currentUser, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
