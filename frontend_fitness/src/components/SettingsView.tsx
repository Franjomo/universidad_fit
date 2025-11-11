import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Separator } from './ui/separator';
import { Badge } from './ui/badge';
import { 
  Settings, 
  Bell, 
  Shield, 
  Database, 
  Mail, 
  Clock,
  Users,
  Activity,
  Save,
  CheckCircle2
} from 'lucide-react';
import { toast } from 'sonner@2.0.3';

export function SettingsView() {
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [weeklyReports, setWeeklyReports] = useState(true);
  const [autoAssignment, setAutoAssignment] = useState(false);
  const [maintenanceMode, setMaintenanceMode] = useState(false);

  const handleSaveSettings = () => {
    toast.success('Configuración guardada exitosamente');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1>Configuración del Sistema</h1>
        <p className="text-gray-600">Administra las configuraciones generales de la plataforma</p>
      </div>

      <Tabs defaultValue="general" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 lg:w-auto">
          <TabsTrigger value="general">
            <Settings className="w-4 h-4 mr-2" />
            General
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <Bell className="w-4 h-4 mr-2" />
            Notificaciones
          </TabsTrigger>
          <TabsTrigger value="security">
            <Shield className="w-4 h-4 mr-2" />
            Seguridad
          </TabsTrigger>
          <TabsTrigger value="system">
            <Database className="w-4 h-4 mr-2" />
            Sistema
          </TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Información General</CardTitle>
              <CardDescription>Configuración básica de la aplicación</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="app-name">Nombre de la Aplicación</Label>
                <Input id="app-name" defaultValue="UniCali Fitness" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="institution">Institución</Label>
                <Input id="institution" defaultValue="Universidad Cali" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="support-email">Email de Soporte</Label>
                <Input 
                  id="support-email" 
                  type="email" 
                  defaultValue="soporte@unicali.edu.co"
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Modo de Mantenimiento</Label>
                  <p className="text-xs text-gray-600">
                    Desactiva temporalmente el acceso al sistema
                  </p>
                </div>
                <Switch
                  checked={maintenanceMode}
                  onCheckedChange={setMaintenanceMode}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Asignación Automática de Entrenadores</Label>
                  <p className="text-xs text-gray-600">
                    Asigna automáticamente entrenadores a nuevos usuarios
                  </p>
                </div>
                <Switch
                  checked={autoAssignment}
                  onCheckedChange={setAutoAssignment}
                />
              </div>

              <Button onClick={handleSaveSettings} className="w-full sm:w-auto">
                <Save className="w-4 h-4 mr-2" />
                Guardar Cambios
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Límites y Restricciones</CardTitle>
              <CardDescription>Configuración de límites del sistema</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="max-routines">Máximo de Rutinas por Usuario</Label>
                <Input 
                  id="max-routines" 
                  type="number" 
                  defaultValue="10" 
                  min="1"
                  max="50"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="max-exercises">Máximo de Ejercicios por Rutina</Label>
                <Input 
                  id="max-exercises" 
                  type="number" 
                  defaultValue="20" 
                  min="5"
                  max="50"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="max-users-per-trainer">Máximo de Usuarios por Entrenador</Label>
                <Input 
                  id="max-users-per-trainer" 
                  type="number" 
                  defaultValue="15" 
                  min="5"
                  max="30"
                />
              </div>

              <Button onClick={handleSaveSettings} className="w-full sm:w-auto">
                <Save className="w-4 h-4 mr-2" />
                Guardar Límites
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Preferencias de Notificaciones</CardTitle>
              <CardDescription>Configura cómo y cuándo enviar notificaciones</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-blue-600" />
                    <Label>Notificaciones por Email</Label>
                  </div>
                  <p className="text-xs text-gray-600">
                    Envía notificaciones importantes por correo electrónico
                  </p>
                </div>
                <Switch
                  checked={emailNotifications}
                  onCheckedChange={setEmailNotifications}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <Bell className="w-4 h-4 text-purple-600" />
                    <Label>Notificaciones Push</Label>
                  </div>
                  <p className="text-xs text-gray-600">
                    Notificaciones en tiempo real en la aplicación
                  </p>
                </div>
                <Switch
                  checked={pushNotifications}
                  onCheckedChange={setPushNotifications}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-green-600" />
                    <Label>Reportes Semanales</Label>
                  </div>
                  <p className="text-xs text-gray-600">
                    Envía resumen semanal de actividad a todos los usuarios
                  </p>
                </div>
                <Switch
                  checked={weeklyReports}
                  onCheckedChange={setWeeklyReports}
                />
              </div>

              <Separator />

              <div className="space-y-2">
                <Label htmlFor="notification-time">Hora de Envío de Reportes</Label>
                <Input 
                  id="notification-time" 
                  type="time" 
                  defaultValue="08:00"
                />
                <p className="text-xs text-gray-600">
                  Los reportes semanales se enviarán todos los lunes a esta hora
                </p>
              </div>

              <Button onClick={handleSaveSettings} className="w-full sm:w-auto">
                <Save className="w-4 h-4 mr-2" />
                Guardar Preferencias
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Configuración de Seguridad</CardTitle>
              <CardDescription>Administra las políticas de seguridad del sistema</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="session-timeout">Tiempo de Inactividad de Sesión (minutos)</Label>
                <Input 
                  id="session-timeout" 
                  type="number" 
                  defaultValue="30" 
                  min="5"
                  max="120"
                />
                <p className="text-xs text-gray-600">
                  Las sesiones inactivas se cerrarán automáticamente después de este tiempo
                </p>
              </div>

              <Separator />

              <div className="space-y-2">
                <Label htmlFor="password-min-length">Longitud Mínima de Contraseña</Label>
                <Input 
                  id="password-min-length" 
                  type="number" 
                  defaultValue="8" 
                  min="6"
                  max="20"
                />
              </div>

              <Separator />

              <div className="space-y-2">
                <Label>Políticas de Contraseña Activas</Label>
                <div className="space-y-2 mt-2">
                  <div className="flex items-center gap-2 text-xs">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    <span className="text-gray-600">Requiere al menos una letra mayúscula</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    <span className="text-gray-600">Requiere al menos un número</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    <span className="text-gray-600">Requiere al menos un carácter especial</span>
                  </div>
                </div>
              </div>

              <Button onClick={handleSaveSettings} className="w-full sm:w-auto">
                <Save className="w-4 h-4 mr-2" />
                Guardar Configuración
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Dominios de Email Autorizados</CardTitle>
              <CardDescription>Solo usuarios con estos dominios pueden registrarse</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary" className="text-xs">
                  @unicali.edu.co
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  @estudiantes.unicali.edu.co
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  @admin.unicali.edu.co
                </Badge>
              </div>
              <Button variant="outline" size="sm">
                Agregar Dominio
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Información del Sistema</CardTitle>
              <CardDescription>Estado y estadísticas del servidor</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label>Versión de la Aplicación</Label>
                  <p className="text-gray-900">v1.0.0</p>
                </div>
                
                <div className="space-y-2">
                  <Label>Última Actualización</Label>
                  <p className="text-gray-900">9 de noviembre, 2024</p>
                </div>

                <div className="space-y-2">
                  <Label>Estado del Servidor</Label>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <p className="text-gray-900">En línea</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Base de Datos</Label>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <p className="text-gray-900">Conectada</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Estadísticas de Uso</CardTitle>
              <CardDescription>Recursos del sistema</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-blue-600" />
                      <Label>Usuarios Registrados</Label>
                    </div>
                    <span className="text-blue-900">47</span>
                  </div>
                </div>

                <Separator />

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-green-600" />
                      <Label>Ejercicios en Biblioteca</Label>
                    </div>
                    <span className="text-green-900">120+</span>
                  </div>
                </div>

                <Separator />

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Database className="w-4 h-4 text-purple-600" />
                      <Label>Espacio de Base de Datos Usado</Label>
                    </div>
                    <span className="text-purple-900">240 MB / 2 GB</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-purple-600 h-2 rounded-full" style={{ width: '12%' }}></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Respaldo y Mantenimiento</CardTitle>
              <CardDescription>Gestión de copias de seguridad</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Último Respaldo</Label>
                <p className="text-gray-900">8 de noviembre, 2024 - 02:00 AM</p>
              </div>

              <div className="space-y-2">
                <Label>Próximo Respaldo Programado</Label>
                <p className="text-gray-900">10 de noviembre, 2024 - 02:00 AM</p>
              </div>

              <Separator />

              <div className="flex gap-2">
                <Button variant="outline">
                  Crear Respaldo Manual
                </Button>
                <Button variant="outline">
                  Restaurar desde Respaldo
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
