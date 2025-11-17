# Frontend Universidad Fit - Documentación

Este documento explica cómo usar los templates HTML y archivos estáticos creados para la aplicación Universidad Fit.

## Estructura de Archivos

```
universidad_fit/
├── templates/
│   ├── base.html                          # Template base con navegación y footer
│   ├── accounts/
│   │   └── login.html                     # Página de inicio de sesión
│   └── fitness/
│       ├── student_dashboard.html         # Dashboard para estudiantes
│       ├── routines_list.html             # Lista de rutinas
│       ├── routine_detail.html            # Detalle de rutina
│       ├── routine_form.html              # Formulario crear/editar rutina
│       ├── exercises_list.html            # Lista de ejercicios
│       ├── exercise_detail.html           # Detalle de ejercicio
│       ├── exercise_form.html             # Formulario crear/editar ejercicio
│       ├── progress_list.html             # Lista de progreso
│       ├── progress_form.html             # Formulario registrar progreso
│       ├── trainer_dashboard.html          # Dashboard para entrenadores
│       ├── trainer_user_progress.html     # Progreso de usuario (entrenador)
│       ├── recommendation_form.html       # Formulario enviar recomendación
│       ├── admin_dashboard.html           # Dashboard administración
│       ├── trainer_management.html        # Gestión de entrenadores
│       ├── reports.html                   # Reportes para usuarios
│       └── admin_reports.html             # Reportes administrativos
├── static/
│   ├── css/
│   │   └── main.css                       # Estilos principales
│   └── js/
│       └── main.js                        # JavaScript principal
```

## Configuración en settings.py

Ya está configurado:
- `TEMPLATES['DIRS']` apunta a `BASE_DIR / 'templates'`
- `STATICFILES_DIRS` incluye `BASE_DIR / 'static'`
- `STATIC_URL = 'static/'`

## Ejemplos de Vistas Django

### 1. Vista de Login

```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')
                if user.role == 'STUDENT' or user.role == 'EMPLOYEE':
                    return redirect('student_dashboard')
                elif user.role == 'ADMIN':
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
```

### 2. Dashboard de Estudiante

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fitness.models import Routine, Progress
from django.utils import timezone
from datetime import timedelta

@login_required
def student_dashboard(request):
    user_id = str(request.user.username)
    
    # Estadísticas
    total_routines = Routine.objects(user_id=user_id).count()
    total_progress = Progress.objects(user_id=user_id).count()
    
    # Entrenamientos esta semana
    week_start = timezone.now() - timedelta(days=7)
    weekly_workouts = Progress.objects(
        user_id=user_id,
        date__gte=week_start
    ).count()
    
    # Días consecutivos (simplificado)
    current_streak = 0  # Implementar lógica según necesidad
    
    # Rutinas recientes
    recent_routines = Routine.objects(
        user_id=user_id
    ).order_by('-created_at')[:5]
    
    # Progreso reciente
    recent_progress = Progress.objects(
        user_id=user_id
    ).order_by('-date')[:5]
    
    # Notificaciones (ejemplo)
    notifications = [
        {
            'title': 'Nuevo Taller de Yoga',
            'message': 'Inscríbete al taller de yoga el próximo viernes',
            'date': timezone.now()
        }
    ]
    
    context = {
        'total_routines': total_routines,
        'total_progress': total_progress,
        'weekly_workouts': weekly_workouts,
        'current_streak': current_streak,
        'recent_routines': recent_routines,
        'recent_progress': recent_progress,
        'notifications': notifications,
    }
    
    return render(request, 'fitness/student_dashboard.html', context)
```

### 3. Lista de Rutinas

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fitness.models import Routine

@login_required
def routines_list(request):
    user_id = str(request.user.username)
    
    # Obtener todas las rutinas del usuario y plantillas
    routines = Routine.objects(
        __raw__={
            '$or': [
                {'user_id': user_id},
                {'is_template': True}
            ]
        }
    ).order_by('-created_at')
    
    context = {
        'routines': routines,
    }
    
    return render(request, 'fitness/routines_list.html', context)
```

### 4. Formulario de Crear Rutina

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fitness.models import Routine, Exercise

@login_required
def routine_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_template = request.POST.get('is_template') == 'on'
        
        # Procesar ejercicios (formato: exercises[0][exercise_id], etc.)
        exercises = []
        i = 0
        while f'exercises[{i}][exercise_id]' in request.POST:
            exercise_id = request.POST.get(f'exercises[{i}][exercise_id]')
            if exercise_id:
                exercise = Exercise.objects(id=exercise_id).first()
                exercises.append({
                    'exercise_id': exercise_id,
                    'exercise_name': exercise.name if exercise else '',
                    'exercise_type': exercise.type if exercise else '',
                    'sets': int(request.POST.get(f'exercises[{i}][sets]', 0) or 0),
                    'reps': int(request.POST.get(f'exercises[{i}][reps]', 0) or 0),
                    'rest': int(request.POST.get(f'exercises[{i}][rest]', 0) or 0),
                })
            i += 1
        
        routine = Routine(
            name=name,
            description=description,
            exercises=exercises,
            created_by=str(request.user.username),
            user_id=str(request.user.username),
            is_template=is_template
        )
        routine.save()
        
        messages.success(request, 'Rutina creada exitosamente')
        return redirect('routine_detail', routine_id=routine.id)
    
    # Obtener ejercicios disponibles para el formulario
    available_exercises = Exercise.objects.all()
    exercises_json = json.dumps([
        {'id': str(ex.id), 'name': ex.name, 'type': ex.type}
        for ex in available_exercises
    ])
    
    context = {
        'available_exercises': exercises_json,
    }
    
    return render(request, 'fitness/routine_form.html', context)
```

### 5. Reportes con Gráficos

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fitness.models import Progress
from django.utils import timezone
from datetime import timedelta
import json

@login_required
def reports(request):
    user_id = str(request.user.username)
    
    # Progreso semanal (últimas 8 semanas)
    weekly_data = {'labels': [], 'values': []}
    for i in range(8):
        week_start = timezone.now() - timedelta(weeks=8-i, days=timezone.now().weekday())
        week_end = week_start + timedelta(days=7)
        count = Progress.objects(
            user_id=user_id,
            date__gte=week_start,
            date__lt=week_end
        ).count()
        weekly_data['labels'].append(f'Sem {8-i}')
        weekly_data['values'].append(count)
    
    # Distribución por tipo de ejercicio
    # (requiere procesar ejercicios desde rutinas o progreso)
    exercise_type_data = {
        'labels': ['Cardio', 'Fuerza', 'Movilidad'],
        'values': [10, 15, 5]  # Ejemplo, calcular desde datos reales
    }
    
    # Nivel de esfuerzo promedio por semana
    effort_data = {'labels': [], 'values': []}
    for i in range(8):
        week_start = timezone.now() - timedelta(weeks=8-i, days=timezone.now().weekday())
        week_end = week_start + timedelta(days=7)
        progresses = Progress.objects(
            user_id=user_id,
            date__gte=week_start,
            date__lt=week_end
        )
        avg_effort = sum(p.effort_level for p in progresses) / len(progresses) if progresses else 0
        effort_data['labels'].append(f'Sem {8-i}')
        effort_data['values'].append(round(avg_effort, 1))
    
    # Resumen de actividad
    activity_summary = [
        {
            'period': 'Este Mes',
            'total_workouts': Progress.objects(user_id=user_id).count(),
            'total_minutes': sum(p.duration or 0 for p in Progress.objects(user_id=user_id)),
            'avg_effort': 7.5,  # Calcular desde datos
            'routines_completed': 5  # Calcular desde datos
        }
    ]
    
    context = {
        'weekly_progress_data': json.dumps(weekly_data),
        'exercise_type_data': json.dumps(exercise_type_data),
        'effort_level_data': json.dumps(effort_data),
        'activity_summary': activity_summary,
    }
    
    return render(request, 'fitness/reports.html', context)
```

## URLs de Ejemplo

```python
# urls.py principal
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('fitness/', include('fitness.urls')),
]

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

# fitness/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('routines/', views.routines_list, name='routines_list'),
    path('routines/create/', views.routine_create, name='routine_create'),
    path('routines/<str:routine_id>/', views.routine_detail, name='routine_detail'),
    path('routines/<str:routine_id>/edit/', views.routine_edit, name='routine_edit'),
    path('exercises/', views.exercises_list, name='exercises_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<str:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/create/', views.progress_create, name='progress_create'),
    path('reports/', views.reports, name='reports'),
    # URLs para entrenadores
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/users/<str:user_id>/', views.trainer_user_progress, name='trainer_user_progress'),
    # URLs para administración
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/trainers/', views.trainer_management, name='trainer_management'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
]
```

## Notas Importantes

1. **Variables de Contexto**: Todos los templates esperan variables específicas. Asegúrate de pasar todas las variables necesarias desde las vistas.

2. **Formularios**: Los templates usan formularios HTML estándar. Puedes usar Django Forms o procesar manualmente con `request.POST`.

3. **Gráficos**: Los gráficos usan Chart.js (ya incluido en base.html). Pasa los datos como JSON usando `json.dumps()`.

4. **Autenticación**: Usa `@login_required` en todas las vistas que requieren autenticación.

5. **Mensajes**: Usa `messages.success()`, `messages.error()`, etc. para mostrar notificaciones.

6. **IDs de MongoDB**: Los modelos de fitness usan MongoDB (MongoEngine). Los IDs son strings, no enteros.

7. **Responsive**: Todos los templates son responsivos y se adaptan a móviles.

## Personalización

- **Colores**: Modifica las variables CSS en `static/css/main.css` (`:root`)
- **Logo**: Reemplaza el emoji 🏋️ en `base.html` con una imagen
- **Footer**: Actualiza la información de contacto en `base.html`

