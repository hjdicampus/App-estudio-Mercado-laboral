# job_task_platform/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from job_market.models import JobOffer, Skill, MarketTrend
from project_tasks.models import Project, Task
from ai_component.recommendation import TaskRecommender, SkillPredictor
import json
from django.db.models import Count
from django.utils import timezone

@login_required
def dashboard(request):
    # Datos básicos
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    user_tasks = Task.objects.filter(assigned_to=request.user).count()
    total_job_offers = JobOffer.objects.count()
    
    # Estadísticas de tareas
    task_status = Task.objects.values('status').annotate(count=Count('status'))
    task_priority = Task.objects.values('priority').annotate(count=Count('priority'))
    
    # Habilidades más demandadas
    top_skills = Skill.objects.annotate(
        job_count=Count('job_offers')
    ).order_by('-job_count')[:10]
    
    # Comparativa entre plataformas
    platform_stats = JobOffer.objects.values('source__name').annotate(count=Count('id'))
    
    # Recomendaciones de tareas
    recommender = TaskRecommender()
    recommended_tasks = recommender.get_recommendations_for_user(request.user.id)
    
    # Predicciones de habilidades
    skill_predictor = SkillPredictor()
    skill_predictions = skill_predictor.train_model()
    
    # Preparar datos para gráficos
    task_status_data = {
        'labels': [status['status'] for status in task_status],
        'data': [status['count'] for status in task_status]
    }
    
    task_priority_data = {
        'labels': [priority['priority'] for priority in task_priority],
        'data': [priority['count'] for priority in task_priority]
    }
    
    top_skills_data = {
        'labels': [skill.name for skill in top_skills],
        'data': [skill.job_count for skill in top_skills]
    }
    
    platform_stats_data = {
        'labels': [stat['source__name'] for stat in platform_stats],
        'data': [stat['count'] for stat in platform_stats]
    }
    
    # Datos para gráfico de predicciones
    prediction_data = {}
    if skill_predictions:
        for skill, predictions in skill_predictions.items():
            prediction_data[skill] = {
                'dates': [pred[0].strftime('%Y-%m-%d') for pred in predictions],
                'values': [round(float(pred[1]), 2) for pred in predictions]
            }
    
    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'user_tasks': user_tasks,
        'total_job_offers': total_job_offers,
        'task_status_data': json.dumps(task_status_data),
        'task_priority_data': json.dumps(task_priority_data),
        'top_skills_data': json.dumps(top_skills_data),
        'platform_stats_data': json.dumps(platform_stats_data),
        'recommended_tasks': recommended_tasks,
        'prediction_data': json.dumps(prediction_data)
    }
    
    return render(request, 'dashboard.html', context)
