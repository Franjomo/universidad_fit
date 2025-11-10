from django.urls import path
from . import views

urlpatterns = [
    # Exercises
    path('exercises/', views.exercise_list, name='exercise-list'),
    path('exercises/<str:exercise_id>/', views.exercise_detail, name='exercise-detail'),
    
    # Routines
    path('routines/', views.routine_list, name='routine-list'),
    path('routines/<str:routine_id>/', views.routine_detail, name='routine-detail'),
    path('routines/<str:routine_id>/adopt/', views.routine_adopt, name='routine-adopt'),
    
    # Progress
    path('progress/', views.progress_list, name='progress-list'),
    path('progress/<str:progress_id>/', views.progress_detail, name='progress-detail'),
    
    # Recommendations
    path('recommendations/', views.recommendation_list, name='recommendation-list'),
    path('recommendations/<str:recommendation_id>/', views.recommendation_detail, name='recommendation-detail'),
    
    # Follow-ups
    path('followups/', views.followup_list, name='followup-list'),
    path('followups/<str:followup_id>/', views.followup_detail, name='followup-detail'),
]
