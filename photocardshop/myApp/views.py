# myApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import logout

# Registro de usuario
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}")
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado!")
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'user_update.html', {'form': form})
