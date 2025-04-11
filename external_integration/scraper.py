import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from job_market.models import JobOffer, Skill

def scrape_tecnoempleo():
    url = "https://www.tecnoempleo.com/ofertas-trabajo/?tecnologia=django"  # Ejemplo con Django
    headers = {'User-Agent': 'Mozilla/5.0'}  # Evitar bloqueos
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    offers = soup.select('.job-offer')  # Ajusta el selector según la estructura real
    for offer in offers[:5]:  # Limitamos a 5 por ahora
        title = offer.find('h2').text.strip() if offer.find('h2') else "Sin título"
        company = offer.find(class_='company').text.strip() if offer.find(class_='company') else "Sin empresa"
        location = offer.find(class_='location').text.strip() if offer.find(class_='location') else ""
        skills_text = offer.find(class_='skills').text if offer.find(class_='skills') else ""
        skills = [skill.strip() for skill in skills_text.split(',')] if skills_text else []
        link = offer.find('a')['href'] if offer.find('a') else url

        # Guardar en la base de datos
        job, created = JobOffer.objects.get_or_create(
            url=link,
            defaults={
                'title': title,
                'company': company,
                'location': location,
                'salary': '',  # Tecnoempleo no siempre lo muestra
                'date_posted': timezone.now().date(),
                'source': 'Tecnoempleo'
            }
        )
        if created:
            for skill_name in skills:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                job.skills.add(skill)

if __name__ == "__main__":
    scrape_tecnoempleo()