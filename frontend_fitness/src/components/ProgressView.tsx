import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Slider } from './ui/slider';
import { Plus, TrendingUp, Calendar, Activity } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { mockProgressLogs, mockRoutines, mockExercises } from '../lib/mock-data';
import type { ProgressLog } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export function ProgressView() {
  const { currentUser } = useAuth();
  const [progressLogs, setProgressLogs] = useState<ProgressLog[]>(mockProgressLogs);
  const [isLogDialogOpen, setIsLogDialogOpen] = useState(false);

  const [newLog, setNewLog] = useState({
    routineId: '',
    exerciseId: '',
    date: new Date().toISOString().split('T')[0],
    sets: 3,
    reps: 12,
    duration: 10,
    effortLevel: 5,
    notes: ''
  });

  const userLogs = progressLogs.filter(log => log.userId === currentUser?.id);
  const userRoutines = mockRoutines.filter(r => 
    r.userId === currentUser?.id && !r.isPreDesigned
  );

  const selectedRoutine = mockRoutines.find(r => r.id === newLog.routineId);
  const availableExercises = selectedRoutine 
    ? selectedRoutine.exercises.map(e => mockExercises.find(ex => ex.id === e.exerciseId)).filter(Boolean)
    : [];

  const handleLogProgress = () => {
    const log: ProgressLog = {
      id: `pl-${Date.now()}`,
      userId: currentUser?.id || '',
      routineId: newLog.routineId,
      exerciseId: newLog.exerciseId,
      date: new Date(newLog.date),
      sets: newLog.sets,
      reps: newLog.reps,
      duration: newLog.duration,
      effortLevel: newLog.effortLevel,
      notes: newLog.notes
    };

    setProgressLogs([...progressLogs, log]);
    setIsLogDialogOpen(false);
    setNewLog({
      routineId: '',
      exerciseId: '',
      date: new Date().toISOString().split('T')[0],
      sets: 3,
      reps: 12,
      duration: 10,
      effortLevel: 5,
      notes: ''
    });
  };

  // Prepare chart data - progress over time
  const chartData = userLogs
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map(log => ({
      date: new Date(log.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }),
      esfuerzo: log.effortLevel,
      reps: log.reps || 0,
      sets: log.sets || 0
    }));

  // Exercise frequency data
  const exerciseFrequency = userLogs.reduce((acc, log) => {
    const exercise = mockExercises.find(e => e.id === log.exerciseId);
    const name = exercise?.name || 'Desconocido';
    acc[name] = (acc[name] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const frequencyData = Object.entries(exerciseFrequency)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  // Weekly summary
  const thisWeek = new Date();
  thisWeek.setDate(thisWeek.getDate() - 7);
  const weeklyLogs = userLogs.filter(log => new Date(log.date) >= thisWeek);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1>Mi Progreso</h1>
          <p className="text-gray-600">Registra y visualiza tus avances</p>
        </div>
        <Dialog open={isLogDialogOpen} onOpenChange={setIsLogDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Registrar Progreso
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Registrar Progreso</DialogTitle>
              <DialogDescription>
                Documenta tu entrenamiento de hoy
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="log-date">Fecha</Label>
                <Input
                  id="log-date"
                  type="date"
                  value={newLog.date}
                  onChange={(e) => setNewLog({ ...newLog, date: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label>Rutina</Label>
                <Select value={newLog.routineId} onValueChange={(value) => setNewLog({ ...newLog, routineId: value, exerciseId: '' })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona una rutina" />
                  </SelectTrigger>
                  <SelectContent>
                    {userRoutines.map((routine) => (
                      <SelectItem key={routine.id} value={routine.id}>
                        {routine.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {newLog.routineId && (
                <div className="space-y-2">
                  <Label>Ejercicio</Label>
                  <Select value={newLog.exerciseId} onValueChange={(value) => setNewLog({ ...newLog, exerciseId: value })}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona un ejercicio" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableExercises.map((exercise) => (
                        <SelectItem key={exercise!.id} value={exercise!.id}>
                          {exercise!.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="log-sets">Series</Label>
                  <Input
                    id="log-sets"
                    type="number"
                    value={newLog.sets}
                    onChange={(e) => setNewLog({ ...newLog, sets: parseInt(e.target.value) })}
                    min="1"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="log-reps">Repeticiones</Label>
                  <Input
                    id="log-reps"
                    type="number"
                    value={newLog.reps}
                    onChange={(e) => setNewLog({ ...newLog, reps: parseInt(e.target.value) })}
                    min="1"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="log-duration">Duración (minutos)</Label>
                <Input
                  id="log-duration"
                  type="number"
                  value={newLog.duration}
                  onChange={(e) => setNewLog({ ...newLog, duration: parseInt(e.target.value) })}
                  min="1"
                />
              </div>

              <div className="space-y-2">
                <Label>Nivel de Esfuerzo: {newLog.effortLevel}/10</Label>
                <Slider
                  value={[newLog.effortLevel]}
                  onValueChange={(value) => setNewLog({ ...newLog, effortLevel: value[0] })}
                  min={1}
                  max={10}
                  step={1}
                  className="py-4"
                />
                <div className="flex justify-between text-xs text-gray-600">
                  <span>Muy fácil</span>
                  <span>Moderado</span>
                  <span>Máximo</span>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="log-notes">Notas (opcional)</Label>
                <Textarea
                  id="log-notes"
                  value={newLog.notes}
                  onChange={(e) => setNewLog({ ...newLog, notes: e.target.value })}
                  placeholder="¿Cómo te sentiste? ¿Alguna observación?"
                  rows={3}
                />
              </div>

              <div className="flex gap-2 justify-end pt-4 border-t">
                <Button variant="outline" onClick={() => setIsLogDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button 
                  onClick={handleLogProgress} 
                  disabled={!newLog.routineId || !newLog.exerciseId}
                >
                  Guardar Progreso
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Esta Semana</CardTitle>
            <Calendar className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-blue-900">{weeklyLogs.length}</div>
            <p className="text-xs text-gray-600 mt-1">
              Entrenamientos registrados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Total Registros</CardTitle>
            <Activity className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-green-900">{userLogs.length}</div>
            <p className="text-xs text-gray-600 mt-1">
              Desde que iniciaste
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Esfuerzo Promedio</CardTitle>
            <TrendingUp className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-purple-900">
              {userLogs.length > 0 
                ? (userLogs.reduce((sum, log) => sum + log.effortLevel, 0) / userLogs.length).toFixed(1)
                : '0'
              }/10
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Intensidad general
            </p>
          </CardContent>
        </Card>
      </div>

      {userLogs.length > 0 ? (
        <>
          {/* Charts */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Progreso de Esfuerzo</CardTitle>
                <CardDescription>Nivel de esfuerzo a lo largo del tiempo</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 10]} />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="esfuerzo" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      name="Nivel de Esfuerzo"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Ejercicios Más Frecuentes</CardTitle>
                <CardDescription>Top 5 ejercicios más realizados</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={frequencyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#10b981" name="Veces realizado" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Recent Logs */}
          <Card>
            <CardHeader>
              <CardTitle>Historial de Entrenamientos</CardTitle>
              <CardDescription>Tus registros más recientes</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {userLogs.slice().reverse().slice(0, 10).map((log) => {
                  const exercise = mockExercises.find(e => e.id === log.exerciseId);
                  const routine = mockRoutines.find(r => r.id === log.routineId);
                  return (
                    <div key={log.id} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <p className="text-gray-900">{exercise?.name}</p>
                          <p className="text-xs text-gray-600">{routine?.name}</p>
                        </div>
                        <Badge variant="secondary">
                          {new Date(log.date).toLocaleDateString('es-ES')}
                        </Badge>
                      </div>
                      <div className="flex gap-4 text-gray-600 mb-2">
                        {log.sets && <span>{log.sets} series</span>}
                        {log.reps && <span>× {log.reps} reps</span>}
                        {log.duration && <span>{log.duration} min</span>}
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-gray-600">Esfuerzo:</span>
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${log.effortLevel * 10}%` }}
                          />
                        </div>
                        <span className="text-gray-900">{log.effortLevel}/10</span>
                      </div>
                      {log.notes && (
                        <p className="text-gray-600 mt-2 text-xs italic border-t pt-2">
                          {log.notes}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">Aún no has registrado ningún progreso</p>
            <Button onClick={() => setIsLogDialogOpen(true)}>
              <Plus className="w-4 h-4 mr-2" />
              Registrar Primer Entrenamiento
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
