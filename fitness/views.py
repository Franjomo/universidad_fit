from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models_sql import ExerciseSQL, RoutineSQL, ProgressSQL, RecommendationSQL
from .serializers_sql import (
    ExerciseSQLSerializer, RoutineSQLSerializer, ProgressSQLSerializer,
    RecommendationSQLSerializer
)


# ============ EXERCISES ============

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def exercise_list(request):
    """List all exercises or create a new one"""
    if request.method == 'GET':
        # Query parameters for filtering
        difficulty = request.GET.get('difficulty')
        exercise_type = request.GET.get('type')
        created_by = request.GET.get('created_by')

        exercises = ExerciseSQL.objects.all()
        if difficulty:
            exercises = exercises.filter(difficulty=difficulty)
        if exercise_type:
            exercises = exercises.filter(type=exercise_type)
        if created_by:
            exercises = exercises.filter(created_by=created_by)

        serializer = ExerciseSQLSerializer(exercises, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExerciseSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def exercise_detail(request, exercise_id):
    """Retrieve, update or delete an exercise"""
    try:
        exercise = ExerciseSQL.objects.get(id=exercise_id)
    except ExerciseSQL.DoesNotExist:
        return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExerciseSQLSerializer(exercise)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExerciseSQLSerializer(exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============ ROUTINES ============

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def routine_list(request):
    """List all routines or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        is_template = request.GET.get('is_template')
        created_by = request.GET.get('created_by')

        routines = RoutineSQL.objects.all()
        if user_id:
            routines = routines.filter(user_id=user_id)
        if is_template is not None:
            routines = routines.filter(is_pre_designed=is_template.lower() == 'true')
        if created_by:
            routines = routines.filter(created_by=created_by)

        serializer = RoutineSQLSerializer(routines, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoutineSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def routine_detail(request, routine_id):
    """Retrieve, update or delete a routine"""
    try:
        routine = RoutineSQL.objects.get(id=routine_id)
    except RoutineSQL.DoesNotExist:
        return Response({'error': 'Routine not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoutineSQLSerializer(routine)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RoutineSQLSerializer(routine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def routine_adopt(request, routine_id):
    """Adopt a template routine for a user"""
    try:
        template = RoutineSQL.objects.get(id=routine_id)
    except RoutineSQL.DoesNotExist:
        return Response({'error': 'Routine not found'}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a copy of the routine for the user
    new_routine = RoutineSQL.objects.create(
        name=template.name,
        description=template.description,
        exercises=template.exercises,
        created_by=user_id,
        is_pre_designed=False,
        base_routine_id=template.id,
        user_id=user_id
    )

    serializer = RoutineSQLSerializer(new_routine)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============ PROGRESS ============

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def progress_list(request):
    """List all progress entries or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        routine_id = request.GET.get('routine_id')
        exercise_id = request.GET.get('exercise_id')

        progress_entries = ProgressSQL.objects.all()
        if user_id:
            progress_entries = progress_entries.filter(user_id=user_id)
        if routine_id:
            progress_entries = progress_entries.filter(routine_id=routine_id)
        if exercise_id:
            progress_entries = progress_entries.filter(exercise_id=exercise_id)

        # Order by date descending
        progress_entries = progress_entries.order_by('-date')

        serializer = ProgressSQLSerializer(progress_entries, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProgressSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def progress_detail(request, progress_id):
    """Retrieve, update or delete a progress entry"""
    try:
        progress = ProgressSQL.objects.get(id=progress_id)
    except ProgressSQL.DoesNotExist:
        return Response({'error': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProgressSQLSerializer(progress)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProgressSQLSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        progress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============ RECOMMENDATIONS ============

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def recommendation_list(request):
    """List all recommendations or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        trainer_id = request.GET.get('trainer_id')

        recommendations = RecommendationSQL.objects.all()
        if user_id:
            recommendations = recommendations.filter(user_id=user_id)
        if trainer_id:
            recommendations = recommendations.filter(trainer_id=trainer_id)

        recommendations = recommendations.order_by('-created_at')

        serializer = RecommendationSQLSerializer(recommendations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecommendationSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow unauthenticated access for testing
def recommendation_detail(request, recommendation_id):
    """Retrieve, update or delete a recommendation"""
    try:
        recommendation = RecommendationSQL.objects.get(id=recommendation_id)
    except RecommendationSQL.DoesNotExist:
        return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecommendationSQLSerializer(recommendation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RecommendationSQLSerializer(recommendation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recommendation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
