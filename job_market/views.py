from django.shortcuts import render
from django.db.models import Count
from .models import JobOffer, Skill

def dashboard(request):
    # Obtener las 10 habilidades más demandadas
    skills = Skill.objects.annotate(num_offers=Count('joboffer')).order_by('-num_offers')[:10]
    # Contar el total de ofertas
    total_offers = JobOffer.objects.count()
    context = {
        'skills': skills,
        'total_offers': total_offers,
    }
    return render(request, 'job_market/dashboard.html', context)