import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Search, Plus, Clock, Activity, TrendingUp } from 'lucide-react';
import { exercisesAPI } from '../lib/api';
import { useExercises } from '../hooks/useFitnessData';
import type { Exercise, ExerciseType, DifficultyLevel } from '../types';
import { useAuth } from '../contexts/AuthContext';

export function ExerciseLibrary() {
  const { currentUser } = useAuth();
  const { exercises, loading, error, refetch } = useExercises();
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all');
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);

  // New exercise form state
  const [newExercise, setNewExercise] = useState({
    name: '',
    type: 'cardio' as ExerciseType,
    description: '',
    duration: 10,
    difficulty: 'principiante' as DifficultyLevel,
    videoUrl: ''
  });

  const filteredExercises = exercises.filter(exercise => {
    const matchesSearch = exercise.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         exercise.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === 'all' || exercise.type === typeFilter;
    const matchesDifficulty = difficultyFilter === 'all' || exercise.difficulty === difficultyFilter;
    
    return matchesSearch && matchesType && matchesDifficulty;
  });

  const getTypeColor = (type: ExerciseType) => {
    switch (type) {
      case 'cardio': return 'bg-red-100 text-red-800';
      case 'fuerza': return 'bg-blue-100 text-blue-800';
      case 'movilidad': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyColor = (difficulty: DifficultyLevel) => {
    switch (difficulty) {
      case 'principiante': return 'bg-green-100 text-green-800';
      case 'intermedio': return 'bg-yellow-100 text-yellow-800';
      case 'avanzado': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleAddExercise = async () => {
    try {
      await exercisesAPI.create({
        ...newExercise,
        created_by: currentUser?.id || 'system',
      });

      // Refetch exercises to update the list
      await refetch();
      setIsAddDialogOpen(false);

      // Reset form
      setNewExercise({
        name: '',
        type: 'cardio',
        description: '',
        duration: 10,
        difficulty: 'principiante',
        videoUrl: ''
      });
    } catch (error) {
      console.error('Failed to create exercise:', error);
      alert('Error al crear el ejercicio. Por favor, intenta de nuevo.');
    }
  };

  const canAddExercise = currentUser?.role === 'instructor' || currentUser?.role === 'admin';

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-600">Cargando ejercicios...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-red-600 mb-4">Error al cargar ejercicios: {error}</p>
          <Button onClick={refetch}>Reintentar</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1>Biblioteca de Ejercicios</h1>
          <p className="text-gray-600">Explora y descubre ejercicios para tus rutinas</p>
        </div>
        {canAddExercise && (
          <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Agregar Ejercicio
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Nuevo Ejercicio</DialogTitle>
                <DialogDescription>
                  Crea un nuevo ejercicio personalizado para la biblioteca
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="ex-name">Nombre del Ejercicio</Label>
                  <Input
                    id="ex-name"
                    value={newExercise.name}
                    onChange={(e) => setNewExercise({ ...newExercise, name: e.target.value })}
                    placeholder="Ej: Sentadillas con salto"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Tipo</Label>
                    <Select
                      value={newExercise.type}
                      onValueChange={(value: ExerciseType) => setNewExercise({ ...newExercise, type: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="cardio">Cardio</SelectItem>
                        <SelectItem value="fuerza">Fuerza</SelectItem>
                        <SelectItem value="movilidad">Movilidad</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Dificultad</Label>
                    <Select
                      value={newExercise.difficulty}
                      onValueChange={(value: DifficultyLevel) => setNewExercise({ ...newExercise, difficulty: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="principiante">Principiante</SelectItem>
                        <SelectItem value="intermedio">Intermedio</SelectItem>
                        <SelectItem value="avanzado">Avanzado</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ex-duration">Duración estimada (minutos)</Label>
                  <Input
                    id="ex-duration"
                    type="number"
                    value={newExercise.duration}
                    onChange={(e) => setNewExercise({ ...newExercise, duration: parseInt(e.target.value) })}
                    min="1"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ex-description">Descripción</Label>
                  <Textarea
                    id="ex-description"
                    value={newExercise.description}
                    onChange={(e) => setNewExercise({ ...newExercise, description: e.target.value })}
                    placeholder="Describe el ejercicio, técnica correcta, etc."
                    rows={4}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ex-video">URL del Video (opcional)</Label>
                  <Input
                    id="ex-video"
                    value={newExercise.videoUrl}
                    onChange={(e) => setNewExercise({ ...newExercise, videoUrl: e.target.value })}
                    placeholder="https://youtube.com/..."
                  />
                </div>

                <div className="flex gap-2 justify-end">
                  <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                    Cancelar
                  </Button>
                  <Button onClick={handleAddExercise} disabled={!newExercise.name || !newExercise.description}>
                    Crear Ejercicio
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        )}
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Buscar ejercicios..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Tipo de ejercicio" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los tipos</SelectItem>
                <SelectItem value="cardio">Cardio</SelectItem>
                <SelectItem value="fuerza">Fuerza</SelectItem>
                <SelectItem value="movilidad">Movilidad</SelectItem>
              </SelectContent>
            </Select>

            <Select value={difficultyFilter} onValueChange={setDifficultyFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Dificultad" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas las dificultades</SelectItem>
                <SelectItem value="principiante">Principiante</SelectItem>
                <SelectItem value="intermedio">Intermedio</SelectItem>
                <SelectItem value="avanzado">Avanzado</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Exercise Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredExercises.map((exercise) => (
          <Card key={exercise.id} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setSelectedExercise(exercise)}>
            <CardHeader>
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="line-clamp-1">{exercise.name}</CardTitle>
                {exercise.isCustom && (
                  <Badge variant="secondary" className="shrink-0">Personalizado</Badge>
                )}
              </div>
              <div className="flex gap-2 flex-wrap">
                <Badge className={getTypeColor(exercise.type)}>{exercise.type}</Badge>
                <Badge className={getDifficultyColor(exercise.difficulty)}>{exercise.difficulty}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 line-clamp-2 mb-4">{exercise.description}</p>
              <div className="flex items-center gap-4 text-gray-600">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>{exercise.duration} min</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredExercises.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No se encontraron ejercicios con los filtros seleccionados</p>
          </CardContent>
        </Card>
      )}

      {/* Exercise Detail Dialog */}
      {selectedExercise && (
        <Dialog open={!!selectedExercise} onOpenChange={() => setSelectedExercise(null)}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>{selectedExercise.name}</DialogTitle>
              <div className="flex gap-2 pt-2">
                <Badge className={getTypeColor(selectedExercise.type)}>{selectedExercise.type}</Badge>
                <Badge className={getDifficultyColor(selectedExercise.difficulty)}>{selectedExercise.difficulty}</Badge>
              </div>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <h4 className="mb-2">Descripción</h4>
                <p className="text-gray-600">{selectedExercise.description}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-gray-600 mb-1">
                    <Clock className="w-4 h-4" />
                    <span>Duración</span>
                  </div>
                  <p className="text-gray-900">{selectedExercise.duration} minutos</p>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-gray-600 mb-1">
                    <TrendingUp className="w-4 h-4" />
                    <span>Nivel</span>
                  </div>
                  <p className="text-gray-900 capitalize">{selectedExercise.difficulty}</p>
                </div>
              </div>

              {selectedExercise.videoUrl && (
                <div>
                  <h4 className="mb-2">Video Demostrativo</h4>
                  <Button variant="outline" className="w-full" asChild>
                    <a href={selectedExercise.videoUrl} target="_blank" rel="noopener noreferrer">
                      Ver Video
                    </a>
                  </Button>
                </div>
              )}
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}
