from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Rutinas
    path('routines/', views.routines_list, name='routines_list'),
    path('routines/create/', views.routine_create, name='routine_create'),
    path('routines/<str:routine_id>/', views.routine_detail, name='routine_detail'),
    
    # Ejercicios
    path('exercises/', views.exercises_list, name='exercises_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<str:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    
    # Progreso
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/create/', views.progress_create, name='progress_create'),
    
    # Reportes
    path('reports/', views.reports, name='reports'),
    
    # Entrenadores
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    
    # Administración
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/trainers/', views.trainer_management, name='trainer_management'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
]

