import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Users, UserCheck, Activity, TrendingUp } from 'lucide-react';
import { mockUsers, mockUserStatistics, mockInstructorStatistics } from '../lib/mock-data';
import type { User } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export function AdminDashboard() {
  const [users, setUsers] = useState<User[]>(mockUsers);
  const [assignmentChanges, setAssignmentChanges] = useState<Record<string, string>>({});

  const instructors = users.filter(u => u.role === 'instructor');
  const studentsAndEmployees = users.filter(u => u.role === 'student' || u.role === 'employee');

  const handleAssignmentChange = (userId: string, trainerId: string) => {
    setAssignmentChanges({
      ...assignmentChanges,
      [userId]: trainerId
    });
  };

  const handleSaveAssignments = () => {
    const updatedUsers = users.map(user => {
      if (assignmentChanges[user.id]) {
        return {
          ...user,
          assignedTrainerId: assignmentChanges[user.id] === 'none' ? undefined : assignmentChanges[user.id]
        };
      }
      return user;
    });

    setUsers(updatedUsers);
    setAssignmentChanges({});
  };

  const getAssignedCount = (trainerId: string) => {
    return users.filter(u => u.assignedTrainerId === trainerId).length;
  };

  // Monthly statistics data
  const monthlyData = [
    { month: 'Oct', usuarios: 15, entrenamientos: 120 },
    { month: 'Nov', usuarios: 18, entrenamientos: 145 }
  ];

  // User statistics aggregation
  const totalRoutinesStarted = mockUserStatistics.reduce((sum, stat) => sum + stat.routinesStarted, 0);
  const totalProgressLogs = mockUserStatistics.reduce((sum, stat) => sum + stat.progressLogs, 0);

  // Instructor statistics
  const totalAssignments = mockInstructorStatistics.reduce((sum, stat) => sum + stat.newAssignments, 0);
  const totalFollowUps = mockInstructorStatistics.reduce((sum, stat) => sum + stat.followUps, 0);

  const getInitials = (user: User) => {
    return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1>Panel de Administración</h1>
        <p className="text-gray-600">Gestión de usuarios y asignaciones de entrenadores</p>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-6 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Total Usuarios</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-blue-900">{studentsAndEmployees.length}</div>
            <p className="text-xs text-gray-600 mt-1">Estudiantes y colaboradores</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Entrenadores</CardTitle>
            <UserCheck className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-green-900">{instructors.length}</div>
            <p className="text-xs text-gray-600 mt-1">Activos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Rutinas Iniciadas</CardTitle>
            <Activity className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-purple-900">{totalRoutinesStarted}</div>
            <p className="text-xs text-gray-600 mt-1">Total del sistema</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Seguimientos</CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-orange-900">{totalFollowUps}</div>
            <p className="text-xs text-gray-600 mt-1">Por entrenadores</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Actividad Mensual</CardTitle>
            <CardDescription>Usuarios activos y entrenamientos registrados</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="usuarios" fill="#3b82f6" name="Usuarios Activos" />
                <Bar dataKey="entrenamientos" fill="#10b981" name="Entrenamientos" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Carga de Trabajo de Entrenadores</CardTitle>
            <CardDescription>Usuarios asignados por entrenador</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {instructors.map((instructor) => {
                const assignedCount = getAssignedCount(instructor.id);
                return (
                  <div key={instructor.id} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="text-xs">{getInitials(instructor)}</AvatarFallback>
                        </Avatar>
                        <span className="text-gray-900">
                          {instructor.firstName} {instructor.lastName}
                        </span>
                      </div>
                      <Badge>{assignedCount} usuarios</Badge>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${Math.min((assignedCount / 10) * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Assignment Management */}
      <Card>
        <CardHeader>
          <CardTitle>Asignación de Entrenadores</CardTitle>
          <CardDescription>Asigna o modifica entrenadores para cada usuario</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Usuario</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Entrenador Actual</TableHead>
                <TableHead>Nuevo Entrenador</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {studentsAndEmployees.map((user) => {
                const currentTrainer = users.find(u => u.id === user.assignedTrainerId);
                const pendingChange = assignmentChanges[user.id];
                
                return (
                  <TableRow key={user.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="text-xs">{getInitials(user)}</AvatarFallback>
                        </Avatar>
                        <span>{user.firstName} {user.lastName}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary">
                        {user.role === 'student' ? 'Estudiante' : 'Colaborador'}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-gray-600">{user.email}</TableCell>
                    <TableCell>
                      {currentTrainer ? (
                        <span className="text-gray-900">
                          {currentTrainer.firstName} {currentTrainer.lastName}
                        </span>
                      ) : (
                        <span className="text-gray-500 italic">Sin asignar</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <Select
                        value={pendingChange || user.assignedTrainerId || 'none'}
                        onValueChange={(value) => handleAssignmentChange(user.id, value)}
                      >
                        <SelectTrigger className="w-[200px]">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="none">Sin asignar</SelectItem>
                          {instructors.map((instructor) => (
                            <SelectItem key={instructor.id} value={instructor.id}>
                              {instructor.firstName} {instructor.lastName}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>

          {Object.keys(assignmentChanges).length > 0 && (
            <div className="flex justify-end gap-2 mt-4 pt-4 border-t">
              <Button variant="outline" onClick={() => setAssignmentChanges({})}>
                Cancelar Cambios
              </Button>
              <Button onClick={handleSaveAssignments}>
                Guardar Asignaciones ({Object.keys(assignmentChanges).length})
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
