import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Plus, Dumbbell, Calendar, Copy, Trash2, Edit } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { mockRoutines, mockExercises } from '../lib/mock-data';
import type { Routine, RoutineExercise, Exercise } from '../types';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

export function RoutinesView() {
  const { currentUser } = useAuth();
  const [routines, setRoutines] = useState<Routine[]>(mockRoutines);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedRoutine, setSelectedRoutine] = useState<Routine | null>(null);
  
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

  const myRoutines = routines.filter(r => 
    r.userId === currentUser?.id && !r.isPreDesigned
  );

  const preDesignedRoutines = routines.filter(r => r.isPreDesigned);

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

    // Reset
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
      id: `r-${Date.now()}`,
      name: newRoutine.name,
      description: newRoutine.description,
      userId: currentUser?.id || '',
      exercises: newRoutine.exercises,
      isPreDesigned: false,
      createdBy: currentUser?.id || '',
      createdAt: new Date()
    };

    setRoutines([...routines, routine]);
    setIsCreateDialogOpen(false);
    setNewRoutine({ name: '', description: '', exercises: [] });
  };

  const handleAdoptRoutine = (routine: Routine) => {
    const adoptedRoutine: Routine = {
      ...routine,
      id: `r-adopted-${Date.now()}`,
      name: `${routine.name} (Mi copia)`,
      userId: currentUser?.id || '',
      isPreDesigned: false,
      baseRoutineId: routine.id,
      createdAt: new Date()
    };

    setRoutines([...routines, adoptedRoutine]);
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
          <h1>Mis Rutinas</h1>
          <p className="text-gray-600">Crea y gestiona tus rutinas de entrenamiento</p>
        </div>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Nueva Rutina
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Crear Nueva Rutina</DialogTitle>
              <DialogDescription>
                Diseña tu rutina personalizada seleccionando ejercicios
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="routine-name">Nombre de la Rutina</Label>
                <Input
                  id="routine-name"
                  value={newRoutine.name}
                  onChange={(e) => setNewRoutine({ ...newRoutine, name: e.target.value })}
                  placeholder="Ej: Rutina de Fuerza Lunes"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="routine-desc">Descripción</Label>
                <Textarea
                  id="routine-desc"
                  value={newRoutine.description}
                  onChange={(e) => setNewRoutine({ ...newRoutine, description: e.target.value })}
                  placeholder="Describe el objetivo de esta rutina..."
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

      <Tabs defaultValue="my-routines" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="my-routines">Mis Rutinas ({myRoutines.length})</TabsTrigger>
          <TabsTrigger value="pre-designed">Prediseñadas ({preDesignedRoutines.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="my-routines" className="space-y-4">
          {myRoutines.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {myRoutines.map((routine) => (
                <Card key={routine.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle>{routine.name}</CardTitle>
                        <CardDescription className="mt-1">{routine.description}</CardDescription>
                      </div>
                      {routine.baseRoutineId && (
                        <Badge variant="secondary">Adaptada</Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center gap-4 text-gray-600">
                        <div className="flex items-center gap-1">
                          <Dumbbell className="w-4 h-4" />
                          <span>{routine.exercises.length} ejercicios</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          <span>{new Date(routine.createdAt).toLocaleDateString('es-ES')}</span>
                        </div>
                      </div>

                      <div className="border-t pt-3">
                        <p className="text-xs text-gray-600 mb-2">Ejercicios:</p>
                        <div className="space-y-1">
                          {routine.exercises.slice(0, 3).map((ex, idx) => (
                            <p key={idx} className="text-gray-900">
                              • {getExerciseName(ex.exerciseId)}
                            </p>
                          ))}
                          {routine.exercises.length > 3 && (
                            <p className="text-gray-600">
                              +{routine.exercises.length - 3} más
                            </p>
                          )}
                        </div>
                      </div>

                      <Button variant="outline" className="w-full" onClick={() => setSelectedRoutine(routine)}>
                        Ver Detalles
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <Dumbbell className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">No tienes rutinas personalizadas todavía</p>
                <Button onClick={() => setIsCreateDialogOpen(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Crear Primera Rutina
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="pre-designed" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {preDesignedRoutines.map((routine) => (
              <Card key={routine.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle>{routine.name}</CardTitle>
                      <CardDescription className="mt-1">{routine.description}</CardDescription>
                    </div>
                    <Badge className="bg-purple-100 text-purple-800">Entrenador</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-4 text-gray-600">
                      <div className="flex items-center gap-1">
                        <Dumbbell className="w-4 h-4" />
                        <span>{routine.exercises.length} ejercicios</span>
                      </div>
                    </div>

                    <div className="border-t pt-3">
                      <p className="text-xs text-gray-600 mb-2">Ejercicios:</p>
                      <div className="space-y-1">
                        {routine.exercises.slice(0, 3).map((ex, idx) => (
                          <p key={idx} className="text-gray-900">
                            • {getExerciseName(ex.exerciseId)}
                          </p>
                        ))}
                        {routine.exercises.length > 3 && (
                          <p className="text-gray-600">
                            +{routine.exercises.length - 3} más
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Button variant="outline" className="flex-1" onClick={() => setSelectedRoutine(routine)}>
                        Ver Detalles
                      </Button>
                      <Button className="flex-1" onClick={() => handleAdoptRoutine(routine)}>
                        <Copy className="w-4 h-4 mr-2" />
                        Adoptar
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Routine Detail Dialog */}
      {selectedRoutine && (
        <Dialog open={!!selectedRoutine} onOpenChange={() => setSelectedRoutine(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{selectedRoutine.name}</DialogTitle>
              <DialogDescription>{selectedRoutine.description}</DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <h4 className="mb-3">Ejercicios de la Rutina</h4>
                <div className="space-y-2">
                  {selectedRoutine.exercises.map((ex, index) => {
                    const exercise = mockExercises.find(e => e.id === ex.exerciseId);
                    return (
                      <div key={index} className="border rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <p className="text-gray-900">{exercise?.name}</p>
                          <Badge className="ml-2">
                            {exercise?.type}
                          </Badge>
                        </div>
                        <p className="text-gray-600 mb-2">{exercise?.description}</p>
                        <div className="flex gap-4 text-gray-600">
                          {ex.sets && <span>{ex.sets} series</span>}
                          {ex.reps && <span>× {ex.reps} reps</span>}
                          {ex.duration && <span>{ex.duration} min</span>}
                          {ex.restTime && <span>Descanso: {ex.restTime}s</span>}
                        </div>
                        {ex.notes && (
                          <p className="text-gray-600 mt-2 text-xs italic">{ex.notes}</p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}
