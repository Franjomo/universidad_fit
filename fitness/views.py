from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId
from .models import Exercise, Routine, Progress, Recommendation, FollowUp
from .serializers import (
    ExerciseSerializer, RoutineSerializer, ProgressSerializer,
    RecommendationSerializer, FollowUpSerializer
)


# ============ EXERCISES ============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def exercise_list(request):
    """List all exercises or create a new one"""
    if request.method == 'GET':
        # Query parameters for filtering
        difficulty = request.GET.get('difficulty')
        exercise_type = request.GET.get('type')
        created_by = request.GET.get('created_by')
        
        exercises = Exercise.objects.all()
        if difficulty:
            exercises = exercises.filter(difficulty=difficulty)
        if exercise_type:
            exercises = exercises.filter(type=exercise_type)
        if created_by:
            exercises = exercises.filter(created_by=created_by)
        
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def exercise_detail(request, exercise_id):
    """Retrieve, update or delete an exercise"""
    try:
        exercise = Exercise.objects.get(id=ObjectId(exercise_id))
    except Exercise.DoesNotExist:
        return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ExerciseSerializer(exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============ ROUTINES ============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def routine_list(request):
    """List all routines or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        is_template = request.GET.get('is_template')
        created_by = request.GET.get('created_by')
        
        routines = Routine.objects.all()
        if user_id:
            routines = routines.filter(user_id=user_id)
        if is_template is not None:
            routines = routines.filter(is_template=is_template.lower() == 'true')
        if created_by:
            routines = routines.filter(created_by=created_by)
        
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def routine_detail(request, routine_id):
    """Retrieve, update or delete a routine"""
    try:
        routine = Routine.objects.get(id=ObjectId(routine_id))
    except Routine.DoesNotExist:
        return Response({'error': 'Routine not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RoutineSerializer(routine)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RoutineSerializer(routine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def routine_adopt(request, routine_id):
    """Adopt a template routine for a user"""
    try:
        template = Routine.objects.get(id=ObjectId(routine_id))
    except Routine.DoesNotExist:
        return Response({'error': 'Routine not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create a copy of the routine for the user
    new_routine = Routine(
        name=template.name,
        description=template.description,
        exercises=template.exercises,
        created_by=user_id,
        is_template=False,
        adopted_from=str(template.id),
        user_id=user_id
    )
    new_routine.save()
    
    serializer = RoutineSerializer(new_routine)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============ PROGRESS ============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def progress_list(request):
    """List all progress entries or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        routine_id = request.GET.get('routine_id')
        exercise_id = request.GET.get('exercise_id')
        
        progress_entries = Progress.objects.all()
        if user_id:
            progress_entries = progress_entries.filter(user_id=user_id)
        if routine_id:
            progress_entries = progress_entries.filter(routine_id=routine_id)
        if exercise_id:
            progress_entries = progress_entries.filter(exercise_id=exercise_id)
        
        # Order by date descending
        progress_entries = progress_entries.order_by('-date')
        
        serializer = ProgressSerializer(progress_entries, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def progress_detail(request, progress_id):
    """Retrieve, update or delete a progress entry"""
    try:
        progress = Progress.objects.get(id=ObjectId(progress_id))
    except Progress.DoesNotExist:
        return Response({'error': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProgressSerializer(progress)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProgressSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        progress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============ RECOMMENDATIONS ============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recommendation_list(request):
    """List all recommendations or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        trainer_id = request.GET.get('trainer_id')
        
        recommendations = Recommendation.objects.all()
        if user_id:
            recommendations = recommendations.filter(user_id=user_id)
        if trainer_id:
            recommendations = recommendations.filter(trainer_id=trainer_id)
        
        recommendations = recommendations.order_by('-created_at')
        
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def recommendation_detail(request, recommendation_id):
    """Retrieve, update or delete a recommendation"""
    try:
        recommendation = Recommendation.objects.get(id=ObjectId(recommendation_id))
    except Recommendation.DoesNotExist:
        return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RecommendationSerializer(recommendation)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RecommendationSerializer(recommendation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        recommendation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============ FOLLOW-UPS ============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def followup_list(request):
    """List all follow-ups or create a new one"""
    if request.method == 'GET':
        # Query parameters
        user_id = request.GET.get('user_id')
        trainer_id = request.GET.get('trainer_id')
        
        followups = FollowUp.objects.all()
        if user_id:
            followups = followups.filter(user_id=user_id)
        if trainer_id:
            followups = followups.filter(trainer_id=trainer_id)
        
        followups = followups.order_by('-created_at')
        
        serializer = FollowUpSerializer(followups, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FollowUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def followup_detail(request, followup_id):
    """Retrieve, update or delete a follow-up"""
    try:
        followup = FollowUp.objects.get(id=ObjectId(followup_id))
    except FollowUp.DoesNotExist:
        return Response({'error': 'FollowUp not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FollowUpSerializer(followup)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FollowUpSerializer(followup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        followup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
