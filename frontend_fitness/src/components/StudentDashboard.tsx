import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Activity, TrendingUp, Calendar, Award } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { mockProgressLogs, mockRoutines, mockRecommendations, mockUserStatistics } from '../lib/mock-data';
import { Badge } from './ui/badge';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function StudentDashboard() {
  const { currentUser } = useAuth();

  if (!currentUser) return null;

  const userRoutines = mockRoutines.filter(
    r => r.userId === currentUser.id && !r.isPreDesigned
  );
  
  const userProgress = mockProgressLogs.filter(p => p.userId === currentUser.id);
  
  const userRecommendations = mockRecommendations.filter(r => r.userId === currentUser.id);

  const currentMonthStats = mockUserStatistics.find(
    s => s.userId === currentUser.id && s.month === '2024-11'
  );

  const recentProgress = userProgress.slice(-5).reverse();

  return (
    <div className="space-y-6">
      <div>
        <h1>¡Bienvenido, {currentUser.firstName}!</h1>
        <p className="text-gray-600">Aquí está tu resumen de actividad física</p>
      </div>

      {/* Hero Image */}
      <div className="relative rounded-xl overflow-hidden h-64 bg-gradient-to-r from-blue-600 to-indigo-700">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1750698544932-c7471990f1ca?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmaXRuZXNzJTIwZ3ltJTIwd29ya291dHxlbnwxfHx8fDE3NjI2MTU1Njd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Fitness"
          className="absolute inset-0 w-full h-full object-cover opacity-40"
        />
        <div className="relative h-full flex flex-col justify-center px-8 text-white">
          <h2 className="text-white mb-2">Tu salud es prioridad</h2>
          <p className="text-white/90 max-w-2xl">
            Mantén un estilo de vida activo y saludable con nuestra plataforma de seguimiento fitness
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Rutinas Activas</CardTitle>
            <Activity className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-blue-900">{userRoutines.length}</div>
            <p className="text-xs text-gray-600 mt-1">
              Rutinas personalizadas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Entrenamientos</CardTitle>
            <Calendar className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-green-900">{currentMonthStats?.progressLogs || 0}</div>
            <p className="text-xs text-gray-600 mt-1">
              Este mes
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Recomendaciones</CardTitle>
            <Award className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-orange-900">{userRecommendations.length}</div>
            <p className="text-xs text-gray-600 mt-1">
              De tu entrenador
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle>Progreso</CardTitle>
            <TrendingUp className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-purple-900">+{userProgress.length}</div>
            <p className="text-xs text-gray-600 mt-1">
              Registros totales
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Actividad Reciente</CardTitle>
            <CardDescription>Tus últimos entrenamientos registrados</CardDescription>
          </CardHeader>
          <CardContent>
            {recentProgress.length > 0 ? (
              <div className="space-y-4">
                {recentProgress.map((log) => (
                  <div key={log.id} className="flex items-start gap-3 pb-3 border-b border-gray-100 last:border-0">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Activity className="w-4 h-4 text-blue-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-gray-900">
                        {log.sets ? `${log.sets} series` : `${log.duration} min`}
                      </p>
                      <p className="text-xs text-gray-600">
                        {new Date(log.date).toLocaleDateString('es-ES')}
                      </p>
                    </div>
                    <Badge variant="secondary">
                      Esfuerzo: {log.effortLevel}/10
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">
                No hay registros todavía. ¡Empieza a entrenar!
              </p>
            )}
          </CardContent>
        </Card>

        {/* Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle>Recomendaciones del Entrenador</CardTitle>
            <CardDescription>Feedback personalizado para ti</CardDescription>
          </CardHeader>
          <CardContent>
            {userRecommendations.length > 0 ? (
              <div className="space-y-4">
                {userRecommendations.map((rec) => (
                  <div key={rec.id} className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                    <div className="flex items-start gap-3">
                      <Award className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-900">{rec.message}</p>
                        <p className="text-xs text-gray-600 mt-2">
                          {new Date(rec.date).toLocaleDateString('es-ES')}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">
                Aún no tienes recomendaciones
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
