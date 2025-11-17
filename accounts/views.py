from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        # Redirigir según el rol del usuario
        if request.user.role == 'STUDENT' or request.user.role == 'EMPLOYEE':
            return redirect('student_dashboard')
        elif request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')
                # Redirigir según el rol
                if user.role == 'STUDENT' or user.role == 'EMPLOYEE':
                    return redirect('student_dashboard')
                elif user.role == 'ADMIN':
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor, completa todos los campos')
    
    # Crear un objeto form simulado para el template
    class SimpleForm:
        def __init__(self):
            self.username = type('obj', (object,), {'value': ''})()
            self.password = type('obj', (object,), {'value': ''})()
            self.errors = {}
            self.non_field_errors = lambda: []
    
    form = SimpleForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')
