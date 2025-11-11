import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Users, TrendingUp, Activity, MessageSquare, Award } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { mockUsers, mockProgressLogs, mockRoutines, mockRecommendations, mockInstructorStatistics } from '../lib/mock-data';
import type { User, TrainerRecommendation } from '../types';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function TrainerDashboard() {
  const { currentUser } = useAuth();
  const [recommendations, setRecommendations] = useState<TrainerRecommendation[]>(mockRecommendations);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [newRecommendation, setNewRecommendation] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const assignedUsers = mockUsers.filter(
    u => u.assignedTrainerId === currentUser?.id
  );

  const currentMonthStats = mockInstructorStatistics.find(
    s => s.instructorId === currentUser?.id && s.month === '2024-11'
  );

  const handleSendRecommendation = () => {
    if (!selectedUser) return;
    
    const rec: TrainerRecommendation = {
      id: `rec-${Date.now()}`,
      trainerId: currentUser?.id || '',
      userId: selectedUser.id,
      message: newRecommendation,
      date: new Date()
    };

    setRecommendations([...recommendations, rec]);
    setNewRecommendation('');
    setIsDialogOpen(false);
    setSelectedUser(null);
  };

  const handleOpenDialog = (user: User) => {
    setSelectedUser(user);
    setNewRecommendation('');
    setIsDialogOpen(true);
  };

  const getUserProgress = (userId: string) => {
    return mockProgressLogs.filter(log => log.userId === userId);
  };

  const getUserRoutines = (userId: string) => {
    return mockRoutines.filter(r => r.userId === userId && !r.isPreDesigned);
  };

  const getInitials = (user: User) => {
    return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1>Panel de Entrenador</h1>
        <p className="text-gray-600">Gestiona y da seguimiento a tus usuarios asignados</p>
      </div>

      {/* Hero Section */}
      <div className="relative rounded-xl overflow-hidden h-48 bg-gradient-to-r from-purple-600 to-indigo-700">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1540205453279-389ebbc43b5b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb25hbCUyMHRyYWluZXIlMjBjb2FjaGluZ3xlbnwxfHx8fDE3NjI1ODI0MTd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Training"
          className="absolute inset-0 w-full h-full object-cover opacity-30"
        />
        <div className="relative h-full flex flex-col justify-center px-8 text-white">
          <h2 className="text-white mb-2">Tu impacto es importante</h2>
          <p className="text-white/90 max-w-2xl">
            Guía, motiva y transforma la vida de tus usuarios a través del fitness
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-6 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Usuarios Asignados</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-blue-900">{assignedUsers.length}</div>
            <p className="text-xs text-gray-600 mt-1">Activos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Nuevas Asignaciones</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-green-900">{currentMonthStats?.newAssignments || 0}</div>
            <p className="text-xs text-gray-600 mt-1">Este mes</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Seguimientos</CardTitle>
            <Activity className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-purple-900">{currentMonthStats?.followUps || 0}</div>
            <p className="text-xs text-gray-600 mt-1">Este mes</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Recomendaciones</CardTitle>
            <MessageSquare className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-orange-900">
              {recommendations.filter(r => r.trainerId === currentUser?.id).length}
            </div>
            <p className="text-xs text-gray-600 mt-1">Enviadas</p>
          </CardContent>
        </Card>
      </div>

      {/* Assigned Users */}
      <Card>
        <CardHeader>
          <CardTitle>Mis Usuarios</CardTitle>
          <CardDescription>Usuarios bajo tu supervisión</CardDescription>
        </CardHeader>
        <CardContent>
          {assignedUsers.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {assignedUsers.map((user) => {
                const userProgress = getUserProgress(user.id);
                const userRoutines = getUserRoutines(user.id);
                const lastLog = userProgress[userProgress.length - 1];

                return (
                  <Card key={user.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start gap-3">
                        <Avatar>
                          <AvatarFallback>{getInitials(user)}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <h4 className="text-gray-900">{user.firstName} {user.lastName}</h4>
                          <p className="text-xs text-gray-600">{user.email}</p>
                          <Badge variant="secondary" className="mt-2">
                            {user.role === 'student' ? 'Estudiante' : 'Colaborador'}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-center">
                          <div className="bg-blue-50 rounded-lg p-3">
                            <p className="text-blue-900">{userRoutines.length}</p>
                            <p className="text-xs text-gray-600">Rutinas</p>
                          </div>
                          <div className="bg-green-50 rounded-lg p-3">
                            <p className="text-green-900">{userProgress.length}</p>
                            <p className="text-xs text-gray-600">Registros</p>
                          </div>
                        </div>

                        {lastLog && (
                          <div className="bg-gray-50 rounded-lg p-3">
                            <p className="text-xs text-gray-600 mb-1">Último entrenamiento</p>
                            <p className="text-gray-900">
                              {new Date(lastLog.date).toLocaleDateString('es-ES')}
                            </p>
                            <p className="text-xs text-gray-600 mt-1">
                              Esfuerzo: {lastLog.effortLevel}/10
                            </p>
                          </div>
                        )}

                        <Button 
                          variant="outline" 
                          className="w-full" 
                          onClick={() => handleOpenDialog(user)}
                        >
                          <MessageSquare className="w-4 h-4 mr-2" />
                          Enviar Recomendación
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-12">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No tienes usuarios asignados todavía</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recent Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>Recomendaciones Recientes</CardTitle>
          <CardDescription>Feedback que has enviado</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recommendations
              .filter(r => r.trainerId === currentUser?.id)
              .slice()
              .reverse()
              .slice(0, 5)
              .map((rec) => {
                const user = mockUsers.find(u => u.id === rec.userId);
                return (
                  <div key={rec.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="text-xs">
                            {user ? getInitials(user) : '?'}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-gray-900">
                            {user?.firstName} {user?.lastName}
                          </p>
                          <p className="text-xs text-gray-600">
                            {new Date(rec.date).toLocaleDateString('es-ES')}
                          </p>
                        </div>
                      </div>
                    </div>
                    <p className="text-gray-600">{rec.message}</p>
                  </div>
                );
              })}
          </div>
        </CardContent>
      </Card>

      {/* Recommendation Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Enviar Recomendación</DialogTitle>
            <DialogDescription>
              {selectedUser && `Para ${selectedUser.firstName} ${selectedUser.lastName}`}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="recommendation">Mensaje</Label>
              <Textarea
                id="recommendation"
                value={newRecommendation}
                onChange={(e) => setNewRecommendation(e.target.value)}
                placeholder="Escribe tu recomendación o retroalimentación..."
                rows={5}
              />
            </div>
            <div className="flex gap-2 justify-end">
              <Button
                variant="outline"
                onClick={() => {
                  setIsDialogOpen(false);
                  setSelectedUser(null);
                  setNewRecommendation('');
                }}
              >
                Cancelar
              </Button>
              <Button
                onClick={handleSendRecommendation}
                disabled={!newRecommendation.trim()}
              >
                <Award className="w-4 h-4 mr-2" />
                Enviar
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
