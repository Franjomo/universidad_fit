import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Plus, Dumbbell, Trash2, Sparkles } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { mockRoutines, mockExercises } from '../lib/mock-data';
import type { Routine, RoutineExercise } from '../types';

export function PreDesignedRoutines() {
  const { currentUser } = useAuth();
  const [routines, setRoutines] = useState<Routine[]>(mockRoutines);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const [newRoutine, setNewRoutine] = useState({
    name: '',
    description: '',
    exercises: [] as RoutineExercise[]
  });

  const [selectedExerciseId, setSelectedExerciseId] = useState('');
  const [exerciseDetails, setExerciseDetails] = useState({
    sets: 3,
    reps: 12,
    duration: 10,
    restTime: 60,
    notes: ''
  });

  const preDesignedRoutines = routines.filter(r => 
    r.isPreDesigned && r.createdBy === currentUser?.id
  );

  const getExerciseName = (exerciseId: string) => {
    return mockExercises.find(e => e.id === exerciseId)?.name || 'Ejercicio';
  };

  const handleAddExerciseToRoutine = () => {
    if (!selectedExerciseId) return;

    const newExercise: RoutineExercise = {
      exerciseId: selectedExerciseId,
      sets: exerciseDetails.sets,
      reps: exerciseDetails.reps,
      duration: exerciseDetails.duration,
      restTime: exerciseDetails.restTime,
      notes: exerciseDetails.notes
    };

    setNewRoutine({
      ...newRoutine,
      exercises: [...newRoutine.exercises, newExercise]
    });

    setSelectedExerciseId('');
    setExerciseDetails({
      sets: 3,
      reps: 12,
      duration: 10,
      restTime: 60,
      notes: ''
    });
  };

  const handleCreateRoutine = () => {
    const routine: Routine = {
      id: `r-pre-${Date.now()}`,
      name: newRoutine.name,
      description: newRoutine.description,
      userId: currentUser?.id || '',
      exercises: newRoutine.exercises,
      isPreDesigned: true,
      createdBy: currentUser?.id || '',
      createdAt: new Date()
    };

    setRoutines([...routines, routine]);
    setIsCreateDialogOpen(false);
    setNewRoutine({ name: '', description: '', exercises: [] });
  };

  const handleRemoveExerciseFromNew = (index: number) => {
    setNewRoutine({
      ...newRoutine,
      exercises: newRoutine.exercises.filter((_, i) => i !== index)
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1>Rutinas Prediseñadas</h1>
          <p className="text-gray-600">Crea rutinas para que los usuarios las adopten</p>
        </div>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Nueva Rutina Prediseñada
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Crear Rutina Prediseñada</DialogTitle>
              <DialogDescription>
                Diseña una rutina profesional para tus usuarios
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="routine-name">Nombre de la Rutina</Label>
                <Input
                  id="routine-name"
                  value={newRoutine.name}
                  onChange={(e) => setNewRoutine({ ...newRoutine, name: e.target.value })}
                  placeholder="Ej: Fuerza Total para Principiantes"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="routine-desc">Descripción</Label>
                <Textarea
                  id="routine-desc"
                  value={newRoutine.description}
                  onChange={(e) => setNewRoutine({ ...newRoutine, description: e.target.value })}
                  placeholder="Describe los beneficios y objetivos de esta rutina..."
                  rows={3}
                />
              </div>

              <div className="border-t pt-4">
                <h4 className="mb-4">Agregar Ejercicios</h4>
                
                <div className="space-y-4 mb-4">
                  <div className="space-y-2">
                    <Label>Seleccionar Ejercicio</Label>
                    <Select value={selectedExerciseId} onValueChange={setSelectedExerciseId}>
                      <SelectTrigger>
                        <SelectValue placeholder="Elige un ejercicio" />
                      </SelectTrigger>
                      <SelectContent>
                        {mockExercises.map((exercise) => (
                          <SelectItem key={exercise.id} value={exercise.id}>
                            {exercise.name} ({exercise.type})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {selectedExerciseId && (
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label>Series</Label>
                        <Input
                          type="number"
                          value={exerciseDetails.sets}
                          onChange={(e) => setExerciseDetails({ ...exerciseDetails, sets: parseInt(e.target.value) })}
                          min="1"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Repeticiones</Label>
                        <Input
                          type="number"
                          value={exerciseDetails.reps}
                          onChange={(e) => setExerciseDetails({ ...exerciseDetails, reps: parseInt(e.target.value) })}
                          min="1"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Duración (min)</Label>
                        <Input
                          type="number"
                          value={exerciseDetails.duration}
                          onChange={(e) => setExerciseDetails({ ...exerciseDetails, duration: parseInt(e.target.value) })}
                          min="1"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Descanso (seg)</Label>
                        <Input
                          type="number"
                          value={exerciseDetails.restTime}
                          onChange={(e) => setExerciseDetails({ ...exerciseDetails, restTime: parseInt(e.target.value) })}
                          min="0"
                        />
                      </div>
                    </div>
                  )}

                  {selectedExerciseId && (
                    <Button onClick={handleAddExerciseToRoutine} variant="outline" className="w-full">
                      <Plus className="w-4 h-4 mr-2" />
                      Agregar Ejercicio
                    </Button>
                  )}
                </div>

                {newRoutine.exercises.length > 0 && (
                  <div className="space-y-2">
                    <Label>Ejercicios en la Rutina</Label>
                    <div className="border rounded-lg divide-y">
                      {newRoutine.exercises.map((ex, index) => (
                        <div key={index} className="p-3 flex items-center justify-between">
                          <div>
                            <p className="text-gray-900">{getExerciseName(ex.exerciseId)}</p>
                            <p className="text-xs text-gray-600">
                              {ex.sets && `${ex.sets} series x ${ex.reps} reps`}
                              {ex.duration && ` • ${ex.duration} min`}
                              {ex.restTime && ` • Descanso: ${ex.restTime}s`}
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveExerciseFromNew(index)}
                          >
                            <Trash2 className="w-4 h-4 text-red-600" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex gap-2 justify-end pt-4 border-t">
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button 
                  onClick={handleCreateRoutine} 
                  disabled={!newRoutine.name || newRoutine.exercises.length === 0}
                >
                  Crear Rutina
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {preDesignedRoutines.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2">
          {preDesignedRoutines.map((routine) => (
            <Card key={routine.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-purple-600" />
                      {routine.name}
                    </CardTitle>
                    <CardDescription className="mt-1">{routine.description}</CardDescription>
                  </div>
                  <Badge className="bg-purple-100 text-purple-800">Prediseñada</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Dumbbell className="w-4 h-4" />
                    <span>{routine.exercises.length} ejercicios</span>
                  </div>

                  <div className="border-t pt-3">
                    <p className="text-xs text-gray-600 mb-2">Ejercicios incluidos:</p>
                    <div className="space-y-1">
                      {routine.exercises.map((ex, idx) => {
                        const exercise = mockExercises.find(e => e.id === ex.exerciseId);
                        return (
                          <div key={idx} className="flex items-start gap-2">
                            <span className="text-gray-400">{idx + 1}.</span>
                            <div className="flex-1">
                              <p className="text-gray-900">{exercise?.name}</p>
                              <p className="text-xs text-gray-600">
                                {ex.sets && `${ex.sets}×${ex.reps}`}
                                {ex.duration && ` • ${ex.duration}min`}
                              </p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 mt-3">
                    <p className="text-green-900 flex items-center gap-2">
                      <Sparkles className="w-4 h-4" />
                      Disponible para que los usuarios la adopten
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <Sparkles className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">No has creado rutinas prediseñadas todavía</p>
            <Button onClick={() => setIsCreateDialogOpen(true)}>
              <Plus className="w-4 h-4 mr-2" />
              Crear Primera Rutina
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
