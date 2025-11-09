from rest_framework import serializers
from .models import Exercise, Routine, Progress, Recommendation, FollowUp


class ExerciseSerializer(serializers.Serializer):
    """Serializer for Exercise MongoDB document"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=['cardio', 'fuerza', 'movilidad'])
    description = serializers.CharField(required=False, allow_blank=True)
    duration = serializers.FloatField(required=False, allow_null=True)
    difficulty = serializers.ChoiceField(
        choices=['baja', 'media', 'alta'], 
        required=False, 
        allow_null=True
    )
    video_url = serializers.URLField(required=False, allow_blank=True)
    created_by = serializers.CharField(default='system')
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new exercise in MongoDB"""
        exercise = Exercise(**validated_data)
        exercise.save()
        return exercise
    
    def update(self, instance, validated_data):
        """Update an existing exercise"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dict"""
        return {
            'id': str(instance.id),
            'name': instance.name,
            'type': instance.type,
            'description': instance.description,
            'duration': instance.duration,
            'difficulty': instance.difficulty,
            'video_url': instance.video_url,
            'created_by': instance.created_by,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }


class RoutineExerciseSerializer(serializers.Serializer):
    """Serializer for exercises within a routine"""
    exercise_id = serializers.CharField()
    sets = serializers.IntegerField(min_value=1, required=False)
    reps = serializers.IntegerField(min_value=1, required=False)
    rest = serializers.IntegerField(min_value=0, required=False)  # seconds
    duration = serializers.FloatField(min_value=0, required=False)  # for cardio


class RoutineSerializer(serializers.Serializer):
    """Serializer for Routine MongoDB document"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=120)
    description = serializers.CharField(required=False, allow_blank=True)
    exercises = RoutineExerciseSerializer(many=True, required=False)
    created_by = serializers.CharField()
    is_template = serializers.BooleanField(default=False)
    adopted_from = serializers.CharField(required=False, allow_null=True)
    user_id = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new routine in MongoDB"""
        exercises_data = validated_data.pop('exercises', [])
        routine = Routine(**validated_data)
        routine.exercises = exercises_data
        routine.save()
        return routine
    
    def update(self, instance, validated_data):
        """Update an existing routine"""
        exercises_data = validated_data.pop('exercises', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if exercises_data is not None:
            instance.exercises = exercises_data
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dict"""
        return {
            'id': str(instance.id),
            'name': instance.name,
            'description': instance.description,
            'exercises': instance.exercises,
            'created_by': instance.created_by,
            'is_template': instance.is_template,
            'adopted_from': instance.adopted_from,
            'user_id': instance.user_id,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }


class ProgressSerializer(serializers.Serializer):
    """Serializer for Progress MongoDB document"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    routine_id = serializers.CharField(required=False, allow_null=True)
    exercise_id = serializers.CharField(required=False, allow_null=True)
    date = serializers.DateTimeField(required=False)
    repetitions = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    duration = serializers.FloatField(min_value=0, required=False, allow_null=True)
    effort_level = serializers.IntegerField(min_value=1, max_value=10, required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new progress entry in MongoDB"""
        progress = Progress(**validated_data)
        progress.save()
        return progress
    
    def update(self, instance, validated_data):
        """Update an existing progress entry"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dict"""
        return {
            'id': str(instance.id),
            'user_id': instance.user_id,
            'routine_id': instance.routine_id,
            'exercise_id': instance.exercise_id,
            'date': instance.date.isoformat() if instance.date else None,
            'repetitions': instance.repetitions,
            'duration': instance.duration,
            'effort_level': instance.effort_level,
            'notes': instance.notes,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }


class RecommendationSerializer(serializers.Serializer):
    """Serializer for Recommendation MongoDB document"""
    id = serializers.CharField(read_only=True)
    trainer_id = serializers.CharField()
    user_id = serializers.CharField()
    message = serializers.CharField()
    related_progress_id = serializers.CharField(required=False, allow_null=True)
    related_routine_id = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new recommendation in MongoDB"""
        recommendation = Recommendation(**validated_data)
        recommendation.save()
        return recommendation
    
    def update(self, instance, validated_data):
        """Update an existing recommendation"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dict"""
        return {
            'id': str(instance.id),
            'trainer_id': instance.trainer_id,
            'user_id': instance.user_id,
            'message': instance.message,
            'related_progress_id': instance.related_progress_id,
            'related_routine_id': instance.related_routine_id,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }


class FollowUpSerializer(serializers.Serializer):
    """Serializer for FollowUp MongoDB document"""
    id = serializers.CharField(read_only=True)
    trainer_id = serializers.CharField()
    user_id = serializers.CharField()
    progress_id = serializers.CharField(required=False, allow_null=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new follow-up in MongoDB"""
        followup = FollowUp(**validated_data)
        followup.save()
        return followup
    
    def update(self, instance, validated_data):
        """Update an existing follow-up"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dict"""
        return {
            'id': str(instance.id),
            'trainer_id': instance.trainer_id,
            'user_id': instance.user_id,
            'progress_id': instance.progress_id,
            'comment': instance.comment,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }
