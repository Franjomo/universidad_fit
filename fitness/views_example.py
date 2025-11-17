"""
EJEMPLO DE VISTAS PARA INTEGRAR CON LOS TEMPLATES

Este archivo muestra ejemplos de cómo crear las vistas de Django
para integrar con los templates HTML creados.

IMPORTANTE: Este es solo un ejemplo. Debes adaptar las consultas
a tus modelos reales y agregar la lógica de negocio necesaria.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json

# Importar tus modelos
# from fitness.models import Exercise, Routine, Progress, Recommendation, FollowUp
# from accounts.models import User


# ===== VISTAS DE AUTENTICACIÓN =====

def home(request):
    """Página de inicio"""
    return render(request, 'core/home.html')


def login_view(request):
    """Vista de login - ya implementada en accounts/views.py probablemente"""
    # Ver ejemplo en templates/README.md
    pass


# ===== VISTAS PARA ESTUDIANTES =====

@login_required
def student_dashboard(request):
    """
    Dashboard principal para estudiantes y empleados
    
    Contexto esperado por el template:
    - total_routines: int
    - total_progress: int
    - weekly_workouts: int
    - current_streak: int
    - recent_routines: QuerySet de Routine
    - recent_progress: QuerySet de Progress
    - notifications: list de dicts con 'title', 'message', 'date'
    """
    user_id = str(request.user.username)
    
    # Ejemplo con MongoEngine (ajustar según tus modelos)
    # total_routines = Routine.objects(user_id=user_id).count()
    # total_progress = Progress.objects(user_id=user_id).count()
    
    # Para PostgreSQL (si tienes modelos relacionados)
    # total_routines = Routine.objects.filter(user_id=user_id).count()
    
    context = {
        'total_routines': 0,  # Reemplazar con consulta real
        'total_progress': 0,
        'weekly_workouts': 0,
        'current_streak': 0,
        'recent_routines': [],  # Routine.objects(user_id=user_id).order_by('-created_at')[:5]
        'recent_progress': [],  # Progress.objects(user_id=user_id).order_by('-date')[:5]
        'notifications': [
            {
                'title': 'Nuevo Taller de Yoga',
                'message': 'Inscríbete al taller de yoga el próximo viernes a las 6 PM',
                'date': timezone.now()
            }
        ],
    }
    
    return render(request, 'fitness/student_dashboard.html', context)


@login_required
def routines_list(request):
    """
    Lista todas las rutinas disponibles
    
    Contexto esperado:
    - routines: QuerySet de Routine
    """
    user_id = str(request.user.username)
    
    # Ejemplo: obtener rutinas del usuario y plantillas públicas
    # routines = Routine.objects(
    #     __raw__={
    #         '$or': [
    #             {'user_id': user_id},
    #             {'is_template': True}
    #         ]
    #     }
    # ).order_by('-created_at')
    
    context = {
        'routines': [],  # Reemplazar con consulta real
    }
    
    return render(request, 'fitness/routines_list.html', context)


@login_required
def routine_detail(request, routine_id):
    """
    Detalle de una rutina específica
    
    Contexto esperado:
    - routine: objeto Routine
    """
    # routine = Routine.objects(id=routine_id).first()
    # if not routine:
    #     messages.error(request, 'Rutina no encontrada')
    #     return redirect('routines_list')
    
    context = {
        'routine': None,  # Reemplazar con consulta real
    }
    
    return render(request, 'fitness/routine_detail.html', context)


@login_required
def routine_create(request):
    """
    Crear nueva rutina
    
    GET: muestra formulario
    POST: procesa formulario y crea rutina
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_template = request.POST.get('is_template') == 'on'
        
        # Procesar ejercicios del formulario
        exercises = []
        i = 0
        while f'exercises[{i}][exercise_id]' in request.POST:
            exercise_id = request.POST.get(f'exercises[{i}][exercise_id]')
            if exercise_id:
                # exercise = Exercise.objects(id=exercise_id).first()
                exercises.append({
                    'exercise_id': exercise_id,
                    'exercise_name': '',  # Obtener del ejercicio
                    'exercise_type': '',
                    'sets': int(request.POST.get(f'exercises[{i}][sets]', 0) or 0),
                    'reps': int(request.POST.get(f'exercises[{i}][reps]', 0) or 0),
                    'rest': int(request.POST.get(f'exercises[{i}][rest]', 0) or 0),
                })
            i += 1
        
        # Crear rutina
        # routine = Routine(
        #     name=name,
        #     description=description,
        #     exercises=exercises,
        #     created_by=str(request.user.username),
        #     user_id=str(request.user.username),
        #     is_template=is_template
        # )
        # routine.save()
        
        messages.success(request, 'Rutina creada exitosamente')
        # return redirect('routine_detail', routine_id=routine.id)
        return redirect('routines_list')
    
    # Obtener ejercicios disponibles para el formulario
    # available_exercises = Exercise.objects.all()
    available_exercises = []
    exercises_json = json.dumps([
        {'id': str(ex.id), 'name': ex.name, 'type': ex.type}
        for ex in available_exercises
    ])
    
    context = {
        'available_exercises': exercises_json,
    }
    
    return render(request, 'fitness/routine_form.html', context)


@login_required
def exercises_list(request):
    """
    Lista todos los ejercicios disponibles
    
    Contexto esperado:
    - exercises: QuerySet de Exercise
    """
    # exercises = Exercise.objects.all().order_by('name')
    
    context = {
        'exercises': [],  # Reemplazar con consulta real
    }
    
    return render(request, 'fitness/exercises_list.html', context)


@login_required
def exercise_create(request):
    """
    Crear nuevo ejercicio personalizado
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        exercise_type = request.POST.get('type')
        description = request.POST.get('description', '')
        duration = request.POST.get('duration')
        difficulty = request.POST.get('difficulty', '')
        video_url = request.POST.get('video_url', '')
        
        # exercise = Exercise(
        #     name=name,
        #     type=exercise_type,
        #     description=description,
        #     duration=float(duration) if duration else None,
        #     difficulty=difficulty if difficulty else None,
        #     video_url=video_url if video_url else None,
        #     created_by=str(request.user.username)
        # )
        # exercise.save()
        
        messages.success(request, 'Ejercicio creado exitosamente')
        return redirect('exercises_list')
    
    return render(request, 'fitness/exercise_form.html')


@login_required
def progress_list(request):
    """
    Lista el progreso del usuario
    
    Contexto esperado:
    - progress_list: QuerySet de Progress
    """
    user_id = str(request.user.username)
    
    # progress_list = Progress.objects(user_id=user_id).order_by('-date')
    
    context = {
        'progress_list': [],  # Reemplazar con consulta real
    }
    
    return render(request, 'fitness/progress_list.html', context)


@login_required
def progress_create(request):
    """
    Registrar nuevo progreso
    """
    user_id = str(request.user.username)
    
    if request.method == 'POST':
        routine_id = request.POST.get('routine_id', '')
        exercise_id = request.POST.get('exercise_id', '')
        date = request.POST.get('date')
        repetitions = request.POST.get('repetitions')
        duration = request.POST.get('duration')
        effort_level = int(request.POST.get('effort_level', 5))
        notes = request.POST.get('notes', '')
        
        # progress = Progress(
        #     user_id=user_id,
        #     routine_id=routine_id if routine_id else None,
        #     exercise_id=exercise_id if exercise_id else None,
        #     date=date,
        #     repetitions=int(repetitions) if repetitions else None,
        #     duration=float(duration) if duration else None,
        #     effort_level=effort_level,
        #     notes=notes
        # )
        # progress.save()
        
        messages.success(request, 'Progreso registrado exitosamente')
        return redirect('progress_list')
    
    # Obtener rutinas y ejercicios disponibles
    # available_routines = Routine.objects(user_id=user_id)
    # available_exercises = Exercise.objects.all()
    
    context = {
        'available_routines': [],  # Reemplazar
        'available_exercises': [],  # Reemplazar
    }
    
    return render(request, 'fitness/progress_form.html', context)


@login_required
def reports(request):
    """
    Reportes para usuarios
    
    Contexto esperado:
    - weekly_progress_data: JSON string con 'labels' y 'values'
    - exercise_type_data: JSON string con 'labels' y 'values'
    - effort_level_data: JSON string con 'labels' y 'values'
    - activity_summary: list de dicts
    """
    user_id = str(request.user.username)
    
    # Ejemplo de datos para gráficos
    weekly_data = {
        'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6', 'Sem 7', 'Sem 8'],
        'values': [3, 5, 4, 6, 5, 7, 6, 8]  # Reemplazar con datos reales
    }
    
    exercise_type_data = {
        'labels': ['Cardio', 'Fuerza', 'Movilidad'],
        'values': [10, 15, 5]  # Reemplazar con datos reales
    }
    
    effort_data = {
        'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6', 'Sem 7', 'Sem 8'],
        'values': [6.5, 7.0, 7.2, 7.5, 7.8, 8.0, 8.2, 8.5]  # Reemplazar con datos reales
    }
    
    activity_summary = [
        {
            'period': 'Este Mes',
            'total_workouts': 20,
            'total_minutes': 600,
            'avg_effort': 7.5,
            'routines_completed': 5
        }
    ]
    
    context = {
        'weekly_progress_data': json.dumps(weekly_data),
        'exercise_type_data': json.dumps(exercise_type_data),
        'effort_level_data': json.dumps(effort_data),
        'activity_summary': activity_summary,
    }
    
    return render(request, 'fitness/reports.html', context)


# ===== VISTAS PARA ENTRENADORES =====

@login_required
def trainer_dashboard(request):
    """
    Dashboard para entrenadores
    
    Contexto esperado:
    - assigned_users: int
    - total_routines_created: int
    - total_recommendations: int
    - pending_followups: int
    - assigned_users_list: list de dicts con info de usuarios
    - trainer_routines: QuerySet de Routine
    """
    trainer_id = str(request.user.username)
    
    context = {
        'assigned_users': 0,
        'total_routines_created': 0,
        'total_recommendations': 0,
        'pending_followups': 0,
        'assigned_users_list': [],
        'trainer_routines': [],
    }
    
    return render(request, 'fitness/trainer_dashboard.html', context)


@login_required
def trainer_user_progress(request, user_id):
    """
    Ver progreso de un usuario asignado
    """
    context = {
        'user_data': {
            'user_id': user_id,
            'username': 'usuario_ejemplo',
            'full_name': 'Nombre Usuario',
            'email': 'usuario@icesi.edu.co'
        },
        'progress_summary': {
            'total_workouts': 0,
            'avg_effort': 0,
            'total_duration': 0,
            'last_workout': None
        },
        'progress_list': [],
        'recommendations': [],
    }
    
    return render(request, 'fitness/trainer_user_progress.html', context)


@login_required
def trainer_send_recommendation(request, user_id):
    """
    Enviar recomendación a un usuario
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        related_routine_id = request.POST.get('related_routine_id', '')
        related_progress_id = request.POST.get('related_progress_id', '')
        
        # recommendation = Recommendation(
        #     trainer_id=str(request.user.username),
        #     user_id=user_id,
        #     message=message,
        #     related_routine_id=related_routine_id if related_routine_id else None,
        #     related_progress_id=related_progress_id if related_progress_id else None
        # )
        # recommendation.save()
        
        messages.success(request, 'Recomendación enviada exitosamente')
        return redirect('trainer_user_progress', user_id=user_id)
    
    context = {
        'user_data': {
            'user_id': user_id,
            'full_name': 'Nombre Usuario'
        },
        'available_routines': [],
        'user_progress': [],
    }
    
    return render(request, 'fitness/recommendation_form.html', context)


# ===== VISTAS PARA ADMINISTRACIÓN =====

@login_required
def admin_dashboard(request):
    """
    Dashboard de administración
    """
    if request.user.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('student_dashboard')
    
    context = {
        'total_users': 0,
        'total_trainers': 0,
        'total_routines': 0,
        'total_progress': 0,
    }
    
    return render(request, 'fitness/admin_dashboard.html', context)


@login_required
def trainer_management(request):
    """
    Gestión de entrenadores
    """
    if request.user.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('student_dashboard')
    
    context = {
        'trainers': [],  # Lista de entrenadores con estadísticas
    }
    
    return render(request, 'fitness/trainer_management.html', context)


@login_required
def admin_reports(request):
    """
    Reportes administrativos
    """
    if request.user.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('student_dashboard')
    
    platform_usage_data = {
        'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Usuarios Activos',
            'data': [100, 120, 150, 180, 200, 220],
            'backgroundColor': '#0066cc'
        }]
    }
    
    user_activity_data = {
        'labels': ['Estudiantes', 'Empleados', 'Entrenadores'],
        'datasets': [{
            'label': 'Actividad',
            'data': [500, 200, 50],
            'backgroundColor': ['#0066cc', '#00a86b', '#ff6b35']
        }]
    }
    
    general_stats = [
        {'metric': 'Usuarios Registrados', 'value': 1000, 'change': 5.2},
        {'metric': 'Rutinas Creadas', 'value': 500, 'change': 10.5},
        {'metric': 'Registros de Progreso', 'value': 5000, 'change': 15.3},
    ]
    
    context = {
        'platform_usage_data': json.dumps(platform_usage_data),
        'user_activity_data': json.dumps(user_activity_data),
        'general_stats': general_stats,
    }
    
    return render(request, 'fitness/admin_reports.html', context)

