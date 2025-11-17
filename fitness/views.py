# fitness/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# Importar modelos (descomentar cuando estén disponibles)
# from fitness.models import Exercise, Routine, Progress

@login_required
def student_dashboard(request):
    """Dashboard para estudiantes y empleados"""
    user_id = str(request.user.username)
    
    # Datos de ejemplo - reemplazar con consultas reales a tus modelos
    context = {
        'total_routines': 0,
        'total_progress': 0,
        'weekly_workouts': 0,
        'current_streak': 0,
        'recent_routines': [],
        'recent_progress': [],
        'notifications': [
            {
                'title': 'Bienvenido a Universidad Fit',
                'message': 'Comienza a crear tus rutinas y registra tu progreso',
                'date': timezone.now()
            }
        ],
    }
    
    # Descomentar cuando tengas los modelos configurados:
    # exercises = Exercise.objects(created_by__in=[user_id, "system"])
    # progress = Progress.objects(user_id=user_id).order_by("-date")[:20]
    # context.update({
    #     'total_routines': Routine.objects(user_id=user_id).count(),
    #     'total_progress': Progress.objects(user_id=user_id).count(),
    #     'recent_routines': Routine.objects(user_id=user_id).order_by('-created_at')[:5],
    #     'recent_progress': Progress.objects(user_id=user_id).order_by('-date')[:5],
    # })
    
    return render(request, "fitness/student_dashboard.html", context)


@login_required
def routines_list(request):
    """Lista de rutinas"""
    user_id = str(request.user.username)
    
    context = {
        'routines': [],
    }
    
    # Descomentar cuando tengas los modelos:
    # routines = Routine.objects(
    #     __raw__={
    #         '$or': [
    #             {'user_id': user_id},
    #             {'is_template': True}
    #         ]
    #     }
    # ).order_by('-created_at')
    # context['routines'] = routines
    
    return render(request, 'fitness/routines_list.html', context)


@login_required
def routine_detail(request, routine_id):
    """Detalle de rutina"""
    context = {
        'routine': None,
    }
    
    # Descomentar cuando tengas los modelos:
    # routine = Routine.objects(id=routine_id).first()
    # if not routine:
    #     messages.error(request, 'Rutina no encontrada')
    #     return redirect('routines_list')
    # context['routine'] = routine
    
    return render(request, 'fitness/routine_detail.html', context)


@login_required
def routine_create(request):
    """Crear nueva rutina"""
    if request.method == 'POST':
        # Procesar formulario aquí
        messages.success(request, 'Rutina creada exitosamente')
        return redirect('routines_list')
    
    # Para el formulario, necesitas pasar los ejercicios disponibles
    import json
    context = {
        'available_exercises': json.dumps([]),
    }
    
    return render(request, 'fitness/routine_form.html', context)


@login_required
def exercises_list(request):
    """Lista de ejercicios"""
    context = {
        'exercises': [],
    }
    
    # Descomentar cuando tengas los modelos:
    # exercises = Exercise.objects.all().order_by('name')
    # context['exercises'] = exercises
    
    return render(request, 'fitness/exercises_list.html', context)


@login_required
def exercise_detail(request, exercise_id):
    """Detalle de ejercicio"""
    context = {
        'exercise': None,
    }
    
    return render(request, 'fitness/exercise_detail.html', context)


@login_required
def exercise_create(request):
    """Crear nuevo ejercicio"""
    if request.method == 'POST':
        messages.success(request, 'Ejercicio creado exitosamente')
        return redirect('exercises_list')
    
    return render(request, 'fitness/exercise_form.html')


@login_required
def progress_list(request):
    """Lista de progreso"""
    context = {
        'progress_list': [],
    }
    
    return render(request, 'fitness/progress_list.html', context)


@login_required
def progress_create(request):
    """Registrar nuevo progreso"""
    if request.method == 'POST':
        messages.success(request, 'Progreso registrado exitosamente')
        return redirect('progress_list')
    
    context = {
        'available_routines': [],
        'available_exercises': [],
    }
    
    return render(request, 'fitness/progress_form.html', context)


@login_required
def reports(request):
    """Reportes para usuarios"""
    import json
    
    # Datos de ejemplo para los gráficos
    weekly_data = {
        'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
        'values': [3, 5, 4, 6]
    }
    
    exercise_type_data = {
        'labels': ['Cardio', 'Fuerza', 'Movilidad'],
        'values': [10, 15, 5]
    }
    
    effort_data = {
        'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
        'values': [6.5, 7.0, 7.2, 7.5]
    }
    
    context = {
        'weekly_progress_data': json.dumps(weekly_data),
        'exercise_type_data': json.dumps(exercise_type_data),
        'effort_level_data': json.dumps(effort_data),
        'activity_summary': [
            {
                'period': 'Este Mes',
                'total_workouts': 20,
                'total_minutes': 600,
                'avg_effort': 7.5,
                'routines_completed': 5
            }
        ],
    }
    
    return render(request, 'fitness/reports.html', context)


# ===== VISTAS PARA ENTRENADORES =====

@login_required
def trainer_dashboard(request):
    """Dashboard para entrenadores"""
    context = {
        'assigned_users': 0,
        'total_routines_created': 0,
        'total_recommendations': 0,
        'pending_followups': 0,
        'assigned_users_list': [],
        'trainer_routines': [],
    }
    
    return render(request, 'fitness/trainer_dashboard.html', context)


# ===== VISTAS PARA ADMINISTRACIÓN =====

@login_required
def admin_dashboard(request):
    """Dashboard de administración"""
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
    """Gestión de entrenadores"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('student_dashboard')
    
    context = {
        'trainers': [],
    }
    
    return render(request, 'fitness/trainer_management.html', context)


@login_required
def admin_reports(request):
    """Reportes administrativos"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('student_dashboard')
    
    import json
    
    platform_usage_data = {
        'labels': ['Ene', 'Feb', 'Mar', 'Abr'],
        'datasets': [{
            'label': 'Usuarios Activos',
            'data': [100, 120, 150, 180],
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
    
    context = {
        'platform_usage_data': json.dumps(platform_usage_data),
        'user_activity_data': json.dumps(user_activity_data),
        'general_stats': [
            {'metric': 'Usuarios Registrados', 'value': 1000, 'change': 5.2},
            {'metric': 'Rutinas Creadas', 'value': 500, 'change': 10.5},
        ],
    }
    
    return render(request, 'fitness/admin_reports.html', context)
