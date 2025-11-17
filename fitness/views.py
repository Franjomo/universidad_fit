from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from fitness.forms import ExerciseForm, RoutineForm
from fitness.models import Exercise, Routine, RoutineExercise, Progress  # MongoEngine models

# Importar modelos (descomentar cuando estén disponibles)
# from fitness.models import Exercise, Routine, Progress

@login_required
def student_dashboard(request):
    user_id = str(request.user.username)

    context = {
        'total_routines': Routine.objects(user_id=user_id).count(),
        'total_progress': Progress.objects(user_id=user_id).count(),
        'weekly_workouts': 0,
        'current_streak': 0,
        'recent_routines': Routine.objects(user_id=user_id).order_by("-created_at")[:5],
        'recent_progress': Progress.objects(user_id=user_id).order_by("-date")[:5],
        'notifications': [
            {
                'title': 'Bienvenido a Universidad Fit',
                'message': 'Comienza a crear tus rutinas y registra tu progreso',
                'date': timezone.now()
            }
        ],
    }

    return render(request, "fitness/student_dashboard.html", context)


@login_required
def routines_list(request):
    user_id = str(request.user.username)

    # Mostrar rutinas propias + plantillas
    routines = Routine.objects.filter(
        __raw__={
            "$or": [
                {"created_by": user_id},
                {"is_template": True}
            ]
        }
    ).order_by("-created_at")

    return render(request, "fitness/routines_list.html", {
        "routines": routines
    })

@login_required
def routine_detail(request, routine_id):
    routine = Routine.objects(id=routine_id).first()
    if not routine:
        messages.error(request, "La rutina no existe.")
        return redirect("routines_list")

    return render(request, "fitness/routine_detail.html", {
        "routine": routine
    })

@login_required
def routine_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        is_template = bool(request.POST.get("is_template"))

        exercises_data = []
        for key, value in request.POST.items():
            # detect keys like exercises[1][exercise_id]
            if key.startswith("exercises") and key.endswith("[exercise_id]"):
                index = key.split("[")[1].split("]")[0]

                exercise_id = value
                sets = request.POST.get(f"exercises[{index}][sets]")
                reps = request.POST.get(f"exercises[{index}][reps]")
                rest = request.POST.get(f"exercises[{index}][rest]")

                # Convert to Exercise object
                exercise_obj = Exercise.objects(id=exercise_id).first()

                exercises_data.append(
                    RoutineExercise(
                        exercise=exercise_obj,
                        sets=int(sets) if sets else None,
                        reps=int(reps) if reps else None,
                        rest=int(rest) if rest else None,
                    )
                )

        routine = Routine(
            name=name,
            description=description,
            exercises=exercises_data,
            created_by=str(request.user.username),
            is_template=is_template
        )
        routine.save()
        return redirect("routines_list")

    # GET
    return render(request, "fitness/routine_form.html", {
        "form": RoutineForm(),
        "available_exercises": [
            {"id": str(ex.id), "name": ex.name, "type": ex.type}
            for ex in Exercise.objects()
        ]
    })

@login_required
def routine_edit(request, routine_id):
    routine = Routine.objects(id=routine_id).first()
    if not routine:
        messages.error(request, "Rutina no encontrada.")
        return redirect("routines_list")

    available_exercises = [
        {"id": str(ex.id), "name": ex.name, "type": ex.type}
        for ex in Exercise.objects()
    ]

    if request.method == "POST":
        routine.name = request.POST.get("name")
        routine.description = request.POST.get("description")
        routine.is_template = bool(request.POST.get("is_template"))

        # Procesar ejercicios enviados en el formulario
        updated_exercises = []

        for key, value in request.POST.items():
            if key.startswith("exercises") and key.endswith("[exercise_id]"):
                idx = key.split("[")[1].split("]")[0]

                exercise_id = value
                sets = request.POST.get(f"exercises[{idx}][sets]")
                reps = request.POST.get(f"exercises[{idx}][reps]")
                rest = request.POST.get(f"exercises[{idx}][rest]")

                # Buscar Exercise real
                exercise_obj = Exercise.objects(id=exercise_id).first()

                updated_exercises.append(
                    RoutineExercise(
                        exercise=exercise_obj,
                        sets=int(sets) if sets else None,
                        reps=int(reps) if reps else None,
                        rest=int(rest) if rest else None,
                    )
                )

        routine.exercises = updated_exercises
        routine.save()

        messages.success(request, "Rutina actualizada correctamente.")
        return redirect("routine_detail", routine_id=routine.id)

    return render(request, "fitness/routine_form.html", {
        "routine": routine,
        "available_exercises": available_exercises
    })


@login_required
def exercises_list(request):
    exercises = Exercise.objects().order_by("name")

    return render(request, 'fitness/exercises_list.html', {
        'exercises': exercises
    })


@login_required
def exercise_detail(request, exercise_id):
    exercise = Exercise.objects(id=exercise_id).first()

    if not exercise:
        messages.error(request, "Ejercicio no encontrado")
        return redirect("exercises_list")

    return render(request, 'fitness/exercise_detail.html', {
        'exercise': exercise
    })


@login_required
def exercise_create(request):

    if request.method == 'POST':
        form = ExerciseForm(request.POST)

        if form.is_valid():
            try:
                exercise = Exercise(
                    name=form.cleaned_data["name"],
                    type=form.cleaned_data["type"],
                    description=form.cleaned_data.get("description"),
                    duration=form.cleaned_data.get("duration"),
                    difficulty=form.cleaned_data.get("difficulty"),
                    video_url=form.cleaned_data.get("video_url"),
                    created_by=str(request.user.username),
                )
                exercise.save()  # <-- SE GUARDA EN MONGODB

                messages.success(request, 'Ejercicio creado exitosamente')
                return redirect('exercises_list')

            except Exception as e:
                messages.error(request, f"Error al guardar ejercicio: {e}")

    else:
        form = ExerciseForm()

    return render(request, 'fitness/exercise_form.html', {
        'form': form,
        'exercise': None,
    })

@login_required
def exercise_edit(request, exercise_id):
    exercise = get_object_or_404(Exercise, exercise_id=exercise_id)

    # Validación opcional: Solo quien lo creó puede editar
    if exercise.created_by != request.user.username:
        messages.error(request, "No tienes permiso para editar este ejercicio.")
        return redirect("exercise_detail", exercise_id=exercise_id)

    if request.method == "POST":
        exercise.name = request.POST.get("name")
        exercise.description = request.POST.get("description")
        exercise.video_url = request.POST.get("video_url")
        exercise.save()

        messages.success(request, "Ejercicio actualizado correctamente.")
        return redirect("exercise_detail", exercise_id=exercise_id)

    return render(request, "fitness/exercise_edit.html", {"exercise": exercise})


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
