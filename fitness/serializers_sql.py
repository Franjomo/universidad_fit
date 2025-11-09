from rest_framework import serializers
from .models_sql import ExerciseSQL, RoutineSQL, ProgressSQL, RecommendationSQL


class ExerciseSQLSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    createdBy = serializers.CharField(source='created_by', required=False)
    videoUrl = serializers.URLField(source='video_url', required=False, allow_blank=True)
    isCustom = serializers.BooleanField(source='is_custom', required=False)

    class Meta:
        model = ExerciseSQL
        fields = ['id', 'name', 'type', 'description', 'duration', 'difficulty',
                  'videoUrl', 'createdBy', 'isCustom']


class RoutineSQLSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    createdBy = serializers.CharField(source='created_by')
    isPreDesigned = serializers.BooleanField(source='is_pre_designed', required=False)
    baseRoutineId = serializers.IntegerField(source='base_routine_id', required=False, allow_null=True)
    userId = serializers.CharField(source='user_id', required=False, allow_blank=True)

    class Meta:
        model = RoutineSQL
        fields = ['id', 'name', 'description', 'exercises', 'createdBy',
                  'isPreDesigned', 'baseRoutineId', 'userId']


class ProgressSQLSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    userId = serializers.CharField(source='user_id')
    routineId = serializers.IntegerField(source='routine_id', required=False, allow_null=True)
    exerciseId = serializers.IntegerField(source='exercise_id', required=False, allow_null=True)
    effortLevel = serializers.IntegerField(source='effort_level')

    class Meta:
        model = ProgressSQL
        fields = ['id', 'userId', 'routineId', 'exerciseId', 'date',
                  'sets', 'reps', 'duration', 'effortLevel', 'notes']


class RecommendationSQLSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    trainerId = serializers.CharField(source='trainer_id')
    userId = serializers.CharField(source='user_id')
    routineId = serializers.IntegerField(source='routine_id', required=False, allow_null=True)

    class Meta:
        model = RecommendationSQL
        fields = ['id', 'trainerId', 'userId', 'message', 'routineId', 'date']
