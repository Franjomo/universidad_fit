import { useState, useEffect } from 'react';
import {
  exercisesAPI,
  routinesAPI,
  progressAPI,
  recommendationsAPI
} from '../lib/api';
import type { Exercise, Routine, ProgressLog, TrainerRecommendation } from '../types';

// Hook for exercises
export function useExercises(params?: { difficulty?: string; type?: string; created_by?: string }) {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchExercises = async () => {
    try {
      setLoading(true);
      const data = await exercisesAPI.list(params);
      setExercises(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch exercises');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExercises();
  }, [JSON.stringify(params)]);

  return { exercises, loading, error, refetch: fetchExercises };
}

// Hook for routines
export function useRoutines(params?: { user_id?: string; is_template?: boolean; created_by?: string }) {
  const [routines, setRoutines] = useState<Routine[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRoutines = async () => {
    try {
      setLoading(true);
      const data = await routinesAPI.list(params);
      setRoutines(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch routines');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoutines();
  }, [JSON.stringify(params)]);

  return { routines, loading, error, refetch: fetchRoutines };
}

// Hook for progress logs
export function useProgress(params?: { user_id?: string; routine_id?: string; exercise_id?: string }) {
  const [progressLogs, setProgressLogs] = useState<ProgressLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProgress = async () => {
    try {
      setLoading(true);
      const data = await progressAPI.list(params);
      setProgressLogs(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch progress');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, [JSON.stringify(params)]);

  return { progressLogs, loading, error, refetch: fetchProgress };
}

// Hook for recommendations
export function useRecommendations(params?: { user_id?: string; trainer_id?: string }) {
  const [recommendations, setRecommendations] = useState<TrainerRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const data = await recommendationsAPI.list(params);
      setRecommendations(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [JSON.stringify(params)]);

  return { recommendations, loading, error, refetch: fetchRecommendations };
}
