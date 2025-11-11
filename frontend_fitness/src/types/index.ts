// Types for the fitness tracking application

export type UserRole = 'student' | 'employee' | 'instructor' | 'admin';

export type ExerciseType = 'cardio' | 'fuerza' | 'movilidad';

export type DifficultyLevel = 'principiante' | 'intermedio' | 'avanzado';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  employeeType?: string;
  departmentId?: string;
  programId?: string;
  assignedTrainerId?: string;
}

export interface Exercise {
  id: string;
  name: string;
  type: ExerciseType;
  description: string;
  duration: number; // in minutes
  difficulty: DifficultyLevel;
  videoUrl?: string;
  createdBy?: string; // user id
  isCustom: boolean;
}

export interface RoutineExercise {
  exerciseId: string;
  sets?: number;
  reps?: number;
  duration?: number; // in minutes
  restTime?: number; // in seconds
  notes?: string;
}

export interface Routine {
  id: string;
  name: string;
  description: string;
  userId: string;
  exercises: RoutineExercise[];
  isPreDesigned: boolean;
  createdBy: string; // instructor id for pre-designed routines
  createdAt: Date;
  baseRoutineId?: string; // if adopted from a pre-designed routine
}

export interface ProgressLog {
  id: string;
  userId: string;
  routineId: string;
  exerciseId: string;
  date: Date;
  sets?: number;
  reps?: number;
  duration?: number; // in minutes
  effortLevel: number; // 1-10
  notes?: string;
}

export interface TrainerRecommendation {
  id: string;
  trainerId: string;
  userId: string;
  routineId?: string;
  message: string;
  date: Date;
}

export interface UserStatistics {
  userId: string;
  month: string; // YYYY-MM
  routinesStarted: number;
  progressLogs: number;
}

export interface InstructorStatistics {
  instructorId: string;
  month: string; // YYYY-MM
  newAssignments: number;
  followUps: number;
}
