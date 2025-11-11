import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { Dumbbell, AlertCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const success = await login(email, password);
    if (!success) {
      setError('Credenciales inválidas. Por favor, intenta de nuevo.');
    }
  };

  const quickLogin = (userEmail: string) => {
    setEmail(userEmail);
    setPassword('password123');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Branding */}
        <div className="text-center md:text-left space-y-6">
          <div className="flex items-center justify-center md:justify-start gap-3">
            <div className="bg-blue-600 p-3 rounded-xl">
              <Dumbbell className="w-10 h-10 text-white" />
            </div>
            <div>
              <h1 className="text-blue-900">UniCali Fitness</h1>
              <p className="text-blue-700">Sistema de Bienestar Universitario</p>
            </div>
          </div>
          <div>
            <h2 className="text-blue-900 mb-2">Transforma tu vida universitaria</h2>
            <p className="text-blue-700">
              Registra tus rutinas, monitorea tu progreso y recibe retroalimentación personalizada de entrenadores certificados.
            </p>
          </div>
          <div className="bg-white/50 backdrop-blur rounded-xl p-6 space-y-2">
            <p className="text-blue-900">Acceso rápido (demo):</p>
            <div className="grid gap-2">
              <Button variant="outline" size="sm" onClick={() => quickLogin('juan.perez@unicali.edu.co')}>
                Estudiante
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickLogin('ana.martinez@unicali.edu.co')}>
                Entrenador
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickLogin('admin.bienestar@unicali.edu.co')}>
                Administrador
              </Button>
            </div>
          </div>
        </div>

        {/* Right side - Login Form */}
        <Card className="shadow-2xl">
          <CardHeader>
            <CardTitle>Iniciar Sesión</CardTitle>
            <CardDescription>
              Ingresa con tu cuenta institucional @unicali.edu.co
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              
              <div className="space-y-2">
                <Label htmlFor="email">Correo Institucional</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="usuario@unicali.edu.co"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">Contraseña</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <Button type="submit" className="w-full">
                Ingresar
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
