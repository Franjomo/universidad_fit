# UniCali Fitness - Sistema de Bienestar Universitario

Sistema completo de seguimiento de fitness para la universidad, desarrollado con Django (backend) y React + Vite (frontend).

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración de Bases de Datos](#configuración-de-bases-de-datos)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Usuarios de Prueba](#usuarios-de-prueba)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [APIs Disponibles](#apis-disponibles)
- [Solución de Problemas](#solución-de-problemas)

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8+**
- **Node.js 16+** y **npm** o **yarn**
- **PostgreSQL** (para datos de usuarios)
- **MongoDB** (para datos de fitness)
- **Git**

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd universidad_fit
```

### 2. Configurar Backend (Django)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Frontend (React + Vite)

```bash
cd frontend_fitness
npm install
cd ..
```

## 🗄️ Configuración de Bases de Datos

### PostgreSQL (Datos de Usuarios)

1. Crear base de datos PostgreSQL:

```bash
createdb universidad_fit
# O usando psql:
psql -U postgres
CREATE DATABASE universidad_fit;
```

2. Configurar variables de entorno:

```bash
# Crear archivo .env en la raíz del proyecto
export DATABASE_URL="postgresql://usuario:password@localhost:5432/universidad_fit"
```

### MongoDB (Datos de Fitness)

1. Iniciar MongoDB:

```bash
# En Linux (systemd):
sudo systemctl start mongod

# O usando Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verificar que está corriendo:
mongosh --eval "db.version()"
```

2. Configurar variable de entorno:

```bash
export MONGO_URL="mongodb://localhost:27017/universidad_fit"
```

## 🚀 Ejecución del Proyecto

### 1. Iniciar Backend (Django)

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Aplicar migraciones
python manage.py migrate

# Crear datos de prueba (opcional)
python create_complete_test_data.py
python create_comprehensive_data.py

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

El backend estará disponible en: `http://localhost:8000`

### 2. Iniciar Frontend (React + Vite)

```bash
cd frontend_fitness
npm run dev
```

El frontend estará disponible en: `http://localhost:3001/Fitnesstrackingplatform/`

**Nota:** El frontend está configurado para ejecutarse en el puerto 3001 con la ruta base `/Fitnesstrackingplatform/`.

## 👤 Usuarios de Prueba

El sistema incluye usuarios de prueba para diferentes roles:

### Estudiante
- **Usuario:** `student`
- **Contraseña:** `student123`
- **Email:** `student@unicali.edu.co`
- **Rol:** Estudiante
- **Funcionalidades:**
  - Ver biblioteca de ejercicios
  - Crear y gestionar rutinas personales
  - Registrar progreso de entrenamientos
  - Ver recomendaciones de entrenadores
  - Ver estadísticas de progreso

### Entrenador
- **Usuario:** `trainer`
- **Contraseña:** `trainer123`
- **Email:** `trainer@unicali.edu.co`
- **Rol:** Entrenador (Employee con tipo "Entrenador")
- **Funcionalidades:**
  - Ver usuarios asignados
  - Crear rutinas prediseñadas
  - Enviar recomendaciones a estudiantes
  - Ver seguimiento de progreso de usuarios
  - Gestionar ejercicios

### Administrador
- **Usuario:** `admin` (si está configurado)
- **Contraseña:** `admin123`
- **Rol:** Administrador
- **Funcionalidades:**
  - Gestión completa del sistema
  - Estadísticas globales
  - Ver estadísticas de todos los usuarios
  - Configuración del sistema

## 🔐 Cómo Iniciar Sesión

1. Abre tu navegador y ve a: `http://localhost:3001/Fitnesstrackingplatform/`

2. En la página de login, ingresa:
   - **Correo Institucional:** Puedes usar el username directamente (ej: `student`) o el email completo (ej: `student@unicali.edu.co`)
   - **Contraseña:** La contraseña correspondiente al usuario

3. Haz clic en **"Ingresar"**

4. Serás redirigido al dashboard correspondiente según tu rol:
   - **Estudiantes:** Dashboard con rutinas, ejercicios y progreso
   - **Entrenadores:** Panel de gestión de usuarios y rutinas prediseñadas
   - **Administradores:** Panel administrativo con estadísticas globales

### Acceso Rápido (Demo)

En la página de login, también puedes usar los botones de acceso rápido:
- **Estudiante:** Rellena automáticamente el formulario
- **Entrenador:** Rellena automáticamente el formulario
- **Administrador:** Rellena automáticamente el formulario

## 📁 Estructura del Proyecto

```
universidad_fit/
├── accounts/              # App de autenticación y usuarios
│   ├── models.py         # Modelos User, Student, Employee
│   ├── views.py          # Vistas de login, logout, usuarios
│   └── urls.py           # URLs de autenticación
├── fitness/              # App de datos de fitness
│   ├── models.py         # Modelos MongoDB (Exercise, Routine, Progress, etc.)
│   ├── views.py          # APIs REST para fitness
│   └── urls.py           # URLs de fitness
├── frontend_fitness/      # Frontend React + Vite
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── contexts/    # Contextos (Auth, etc.)
│   │   ├── lib/         # Utilidades y API client
│   │   └── types/       # Tipos TypeScript
│   └── package.json
├── create_complete_test_data.py    # Script para crear usuarios
├── create_comprehensive_data.py    # Script para crear datos de fitness
└── manage.py             # Script de gestión de Django
```

## 🔌 APIs Disponibles

### Autenticación

- `POST /api/accounts/login/` - Iniciar sesión
  ```json
  {
    "email": "student",
    "password": "student123"
  }
  ```

- `POST /api/accounts/logout/` - Cerrar sesión

- `GET /api/accounts/me/` - Obtener usuario actual

### Fitness (MongoDB)

- `GET /api/fitness/exercises/` - Listar ejercicios
- `POST /api/fitness/exercises/` - Crear ejercicio
- `GET /api/fitness/routines/` - Listar rutinas
- `POST /api/fitness/routines/` - Crear rutina
- `GET /api/fitness/progress/` - Listar progreso
- `POST /api/fitness/progress/` - Registrar progreso
- `GET /api/fitness/recommendations/` - Listar recomendaciones
- `POST /api/fitness/recommendations/` - Crear recomendación
- `GET /api/fitness/followups/` - Listar seguimientos
- `POST /api/fitness/followups/` - Crear seguimiento

## 🐛 Solución de Problemas

### Error: "Connection refused" en MongoDB

**Solución:**
```bash
# Verificar que MongoDB está corriendo
sudo systemctl status mongod

# Si no está corriendo, iniciarlo:
sudo systemctl start mongod

# O usando Docker:
docker start mongodb
```

### Error: "No user found" al hacer login

**Solución:**
1. Verifica que los datos de prueba se hayan creado:
   ```bash
   python create_complete_test_data.py
   ```

2. Verifica que el servidor Django se haya reiniciado después de crear usuarios

3. Verifica que estés usando el username correcto (ej: `student`, no `student@unicali.edu.co`)

### Error: CORS en el navegador

**Solución:**
Verifica que `http://localhost:3001` esté en `CORS_ALLOWED_ORIGINS` en `universidad_fit/settings.py`

### El frontend no se conecta al backend

**Solución:**
1. Verifica que el backend esté corriendo en `http://localhost:8000`
2. Verifica que el frontend esté configurado para usar `http://localhost:8000/api` (ver `frontend_fitness/src/lib/api.ts`)
3. Verifica las variables de entorno si están configuradas

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución:**
```bash
# Asegúrate de tener el entorno virtual activado
source venv/bin/activate

# Reinstala las dependencias
pip install -r requirements.txt
```

## 📝 Notas Adicionales

- **Base de datos dual:** El proyecto usa PostgreSQL para datos de usuarios (SQL) y MongoDB para datos de fitness (NoSQL)
- **Autenticación:** Actualmente usa sesiones de Django. Se puede migrar a JWT en el futuro
- **CORS:** Configurado para desarrollo. Ajustar para producción
- **Puertos:** Backend en 8000, Frontend en 3001

## 🎯 Próximos Pasos

1. Implementar autenticación JWT
2. Agregar más validaciones en el frontend
3. Implementar tests automatizados
4. Configurar CI/CD
5. Optimizar consultas a MongoDB
6. Agregar paginación en listas grandes

## 📞 Soporte

Para problemas o preguntas, consulta la documentación de Django y React, o revisa los logs del servidor para más detalles de errores.

---

**Desarrollado para UniCali - Sistema de Bienestar Universitario**

