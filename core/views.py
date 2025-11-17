from django.shortcuts import render

def home(request):
    """Página de inicio"""
    return render(request, 'core/home.html')
