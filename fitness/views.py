# fitness/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fitness.models import Exercise, Progress

@login_required
def dashboard(request):
    user_id = request.user.username
    exercises = Exercise.objects(created_by__in=[user_id, "system"])
    progress = Progress.objects(user_id=user_id).order_by("-date")[:20]
    return render(request, "fitness/dashboard.html", {
        "exercises": exercises,
        "progress": progress,
    })