from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role in ['STUDENT', 'EMPLOYEE']:
            return redirect('student_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('home')
    
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')

                if user.role in ['STUDENT', 'EMPLOYEE']:
                    return redirect('student_dashboard')
                elif user.role == 'ADMIN':
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                form.add_error(None, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, 'Por favor completa los campos correctamente')

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')
