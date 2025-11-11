import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { TrendingUp, TrendingDown, Activity, Users, Target, Award } from 'lucide-react';
import { mockUserStatistics, mockInstructorStatistics, mockUsers, mockProgressLogs, mockRoutines } from '../lib/mock-data';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

export function StatisticsView() {
  // Aggregate user statistics
  const userStatsData = mockUserStatistics.map(stat => ({
    month: stat.month,
    rutinas: stat.routinesStarted,
    seguimientos: stat.progressLogs
  }));

  // Aggregate instructor statistics
  const instructorStatsData = mockInstructorStatistics.map(stat => ({
    month: stat.month,
    asignaciones: stat.newAssignments,
    seguimientos: stat.followUps
  }));

  // Exercise type distribution
  const exercisesByType = mockProgressLogs.reduce((acc, log) => {
    const exercise = mockRoutines
      .flatMap(r => r.exercises)
      .find(e => e.exerciseId === log.exerciseId);
    
    if (exercise) {
      const type = exercise.exerciseId.includes('cardio') ? 'Cardio' : 
                   exercise.exerciseId.includes('fuerza') ? 'Fuerza' : 'Movilidad';
      acc[type] = (acc[type] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  const pieData = Object.entries(exercisesByType).map(([name, value]) => ({
    name,
    value
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b'];

  // Calculate growth
  const octStats = mockUserStatistics.find(s => s.month === '2024-10');
  const novStats = mockUserStatistics.find(s => s.month === '2024-11');
  
  const routineGrowth = octStats && novStats 
    ? ((novStats.routinesStarted - octStats.routinesStarted) / octStats.routinesStarted) * 100 
    : 0;

  // Top users by activity
  const userActivity = mockUsers
    .filter(u => u.role === 'student' || u.role === 'employee')
    .map(user => {
      const logs = mockProgressLogs.filter(l => l.userId === user.id);
      return {
        name: `${user.firstName} ${user.lastName}`,
        registros: logs.length
      };
    })
    .sort((a, b) => b.registros - a.registros)
    .slice(0, 5);

  return (
    <div className="space-y-6">
      <div>
        <h1>Estadísticas del Sistema</h1>
        <p className="text-gray-600">Análisis y métricas de uso de la plataforma</p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Usuarios Activos</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-blue-900">
              {mockUsers.filter(u => u.role !== 'admin' && u.role !== 'instructor').length}
            </div>
            <div className="flex items-center gap-1 mt-1">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <p className="text-xs text-green-600">+20% vs mes anterior</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Rutinas Creadas</CardTitle>
            <Target className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-purple-900">
              {mockUserStatistics.reduce((sum, s) => sum + s.routinesStarted, 0)}
            </div>
            <div className="flex items-center gap-1 mt-1">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <p className="text-xs text-green-600">
                {routineGrowth > 0 ? '+' : ''}{routineGrowth.toFixed(0)}% crecimiento
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Entrenamientos</CardTitle>
            <Activity className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-green-900">
              {mockUserStatistics.reduce((sum, s) => sum + s.progressLogs, 0)}
            </div>
            <div className="flex items-center gap-1 mt-1">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <p className="text-xs text-green-600">+35% en noviembre</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 1 */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Actividad de Usuarios por Mes</CardTitle>
            <CardDescription>Rutinas iniciadas y seguimientos registrados</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={userStatsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="rutinas" fill="#3b82f6" name="Rutinas Iniciadas" />
                <Bar dataKey="seguimientos" fill="#10b981" name="Seguimientos" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Rendimiento de Entrenadores</CardTitle>
            <CardDescription>Asignaciones y seguimientos mensuales</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={instructorStatsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="asignaciones" 
                  stroke="#8b5cf6" 
                  strokeWidth={2}
                  name="Nuevas Asignaciones"
                />
                <Line 
                  type="monotone" 
                  dataKey="seguimientos" 
                  stroke="#f59e0b" 
                  strokeWidth={2}
                  name="Seguimientos Realizados"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top 5 Usuarios Más Activos</CardTitle>
            <CardDescription>Por número de entrenamientos registrados</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={userActivity} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={150} />
                <Tooltip />
                <Bar dataKey="registros" fill="#10b981" name="Registros" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Distribución de Tipos de Ejercicio</CardTitle>
            <CardDescription>Preferencias de entrenamiento</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Statistics Table */}
      <Card>
        <CardHeader>
          <CardTitle>Estadísticas Detalladas por Usuario</CardTitle>
          <CardDescription>Resumen de actividad individual</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {mockUsers
              .filter(u => u.role === 'student' || u.role === 'employee')
              .map(user => {
                const stats = mockUserStatistics.filter(s => s.userId === user.id);
                const totalRoutines = stats.reduce((sum, s) => sum + s.routinesStarted, 0);
                const totalLogs = stats.reduce((sum, s) => sum + s.progressLogs, 0);
                
                return (
                  <div key={user.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <p className="text-gray-900">{user.firstName} {user.lastName}</p>
                        <p className="text-xs text-gray-600">{user.email}</p>
                      </div>
                      <Badge variant="secondary">
                        {user.role === 'student' ? 'Estudiante' : 'Colaborador'}
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-blue-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <Target className="w-4 h-4 text-blue-600" />
                          <p className="text-xs text-gray-600">Rutinas</p>
                        </div>
                        <p className="text-blue-900">{totalRoutines}</p>
                      </div>
                      
                      <div className="bg-green-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <Activity className="w-4 h-4 text-green-600" />
                          <p className="text-xs text-gray-600">Entrenamientos</p>
                        </div>
                        <p className="text-green-900">{totalLogs}</p>
                      </div>

                      <div className="bg-purple-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <Award className="w-4 h-4 text-purple-600" />
                          <p className="text-xs text-gray-600">Mes Actual</p>
                        </div>
                        <p className="text-purple-900">
                          {stats.find(s => s.month === '2024-11')?.progressLogs || 0}
                        </p>
                      </div>

                      <div className="bg-orange-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <TrendingUp className="w-4 h-4 text-orange-600" />
                          <p className="text-xs text-gray-600">Tendencia</p>
                        </div>
                        <p className="text-orange-900 flex items-center gap-1">
                          {totalLogs > 5 ? (
                            <>
                              <TrendingUp className="w-4 h-4" />
                              Alta
                            </>
                          ) : (
                            <>
                              <TrendingDown className="w-4 h-4" />
                              Media
                            </>
                          )}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
