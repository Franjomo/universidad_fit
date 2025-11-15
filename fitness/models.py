from mongoengine import Document, StringField, FloatField, IntField, ListField,DictField, BooleanField, DateTimeField, URLField
from datetime import datetime

class Exercise(Document):
    name = StringField(required=True, max_length=100)
    type = StringField(choices=("cardio", "fuerza", "movilidad"), required=True)
    description = StringField()
    duration = FloatField()
    difficulty = StringField(choices=("baja", "media", "alta"))
    video_url = URLField()
    created_by = StringField(required=True, default="system")  #User ID
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'exercises',
        'indexes': ['difficulty', 'type', 'created_by'],
        'db_alias': 'fitness',  # <- uses the alias configured in connect()
    }

class Routine(Document):
    name = StringField(required=True, max_length=120)
    description = StringField()
    exercises = ListField(DictField())  # [{"exercise_id": "...", "sets": 3, "reps": 12, "rest": 60}]
    created_by = StringField(required=True)  # ID of creator (user or "system")
    is_template = BooleanField(default=False)  # True = prediseñada
    adopted_from = StringField()  # ID de rutina original (si fue copiada)
    user_id = StringField()  # Usuario que la adoptó (si aplica)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'routines',
        'indexes': ['created_by', 'user_id', 'is_template'],
        'db_alias': 'fitness',
    }

class Progress(Document):
    user_id = StringField(required=True)        # ID of user progress belongs to
    routine_id = StringField(required=False)    # ID routine (optional)
    exercise_id = StringField(required=False)   # ID exercise (optional)
    date = DateTimeField(default=datetime.utcnow)
    repetitions = IntField(min_value=0)
    duration = FloatField(min_value=0)          # in seconds
    effort_level = IntField(min_value=1, max_value=10) # 1-10 scale
    notes = StringField() # Additional user notes ("it was tough", "felt great", etc.)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'progress',
        'indexes': ['user_id', 'routine_id', 'date'],
        'db_alias': 'fitness',
    }

class Recommendation(Document):
    trainer_id = StringField(required=True)   # ID instructor (PostgreSQL)
    user_id = StringField(required=True)      # ID user (PostgreSQL)
    message = StringField(required=True)
    related_progress_id = StringField()       # ID de Progress
    related_routine_id = StringField()        # ID de Routine
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'recommendations',
        'indexes': ['trainer_id', 'user_id', 'created_at'],
        'db_alias': 'fitness',
    }

class FollowUp(Document):
    trainer_id = StringField(required=True)   # ID instructor (PostgreSQL)
    user_id = StringField(required=True)      # ID user (PostgreSQL)
    progress_id = StringField(required=False) # Progress ID (MongoDB)
    comment = StringField()                   # Comentarios del instructor
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'followups',
        'indexes': ['trainer_id', 'user_id', 'created_at'],
        'db_alias': 'fitness',
    }