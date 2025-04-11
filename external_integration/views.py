from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .scraper import scrape_tecnoempleo

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def import_jobs(request):
    if request.method == 'POST':
        scrape_tecnoempleo()
        return render(request, 'external_integration/import_success.html', {'message': 'Ofertas importadas con éxito'})
    return render(request, 'external_integration/import.html')