from django.shortcuts import render

def projects_view(request):
    context = {
        'message': 'Gestión de proyectos en desarrollo',
    }
    return render(request, 'project_tasks/projects.html', context)