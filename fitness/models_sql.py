from django.db import models
from datetime import datetime

class ExerciseSQL(models.Model):
    TYPE_CHOICES = [
        ('cardio', 'Cardio'),
        ('fuerza', 'Fuerza'),
        ('movilidad', 'Movilidad'),
    ]

    DIFFICULTY_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    video_url = models.URLField(blank=True)
    created_by = models.CharField(max_length=50, default="system")
    created_at = models.DateTimeField(auto_now_add=True)
    is_custom = models.BooleanField(default=False)

    class Meta:
        db_table = 'fitness_exercises'

    def __str__(self):
        return self.name


class RoutineSQL(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    exercises = models.JSONField(default=list)  # Stores exercise configurations
    created_by = models.CharField(max_length=50)
    is_pre_designed = models.BooleanField(default=False)
    base_routine_id = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_routines'

    def __str__(self):
        return self.name


class ProgressSQL(models.Model):
    user_id = models.CharField(max_length=50)
    routine_id = models.IntegerField(null=True, blank=True)
    exercise_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    effort_level = models.IntegerField(help_text="1-10 scale")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_progress'
        ordering = ['-date']

    def __str__(self):
        return f"Progress for user {self.user_id} on {self.date}"


class RecommendationSQL(models.Model):
    trainer_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    message = models.TextField()
    routine_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_recommendations'
        ordering = ['-created_at']

    def __str__(self):
        return f"Recommendation from {self.trainer_id} to {self.user_id}"
