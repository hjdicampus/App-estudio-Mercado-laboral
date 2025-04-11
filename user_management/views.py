from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'message': 'Bienvenido a la Plataforma de Gestión de Tareas'})