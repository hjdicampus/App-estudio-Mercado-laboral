# external_integration/scrapers.py

import requests
from bs4 import BeautifulSoup
import datetime
from job_market.models import JobOffer, Skill, JobSource, MarketTrend
import logging

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_skills_from_text(self, text):
        """Extrae habilidades del texto de la oferta basado en una lista predefinida"""
        common_skills = ['Python', 'Django', 'JavaScript', 'React', 'Angular', 'Vue', 'SQL', 'PostgreSQL', 
                         'MySQL', 'MongoDB', 'Docker', 'AWS', 'Azure', 'Git', 'CI/CD', 'HTML', 'CSS',
                         'Java', 'C#', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin', 'Flutter', 'React Native']
        
        found_skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                skill_obj, _ = Skill.objects.get_or_create(name=skill)
                found_skills.append(skill_obj)
        
        return found_skills

class TecnoempleoScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.source, _ = JobSource.objects.get_or_create(name=JobSource.TECNOEMPLEO)
    
    def scrape_jobs(self, pages=3):
        jobs = []
        
        for page in range(1, pages + 1):
            url = f"https://www.tecnoempleo.com/ofertas-trabajo/?pagina={page}"
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                job_listings = soup.select('.job-offer')
                
                for job in job_listings:
                    title_elem = job.select_one('.job-offer-title a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    job_url = 'https://www.tecnoempleo.com' + title_elem['href']
                    
                    company_elem = job.select_one('.company-name')
                    company = company_elem.text.strip() if company_elem else "No especificada"
                    
                    location_elem = job.select_one('.job-offer-location')
                    location = location_elem.text.strip() if location_elem else "No especificada"
                    
                    # Obtener detalles adicionales visitando la página de la oferta
                    job_details = self.get_job_details(job_url)
                    
                    # Crear o actualizar la oferta en la base de datos
                    job_offer, created = JobOffer.objects.update_or_create(
                        url=job_url,
                        source=self.source,
                        defaults={
                            'title': title,
                            'company': company,
                            'location': location,
                            'description': job_details['description'],
                            'publication_date': job_details['publication_date'],
                            'salary_min': job_details['salary_min'],
                            'salary_max': job_details['salary_max'],
                            'applicants_count': job_details['applicants_count']
                        }
                    )
                    
                    # Añadir habilidades
                    for skill in job_details['skills']:
                        job_offer.skills_required.add(skill)
                    
                    jobs.append(job_offer)
                    
                    # Actualizar tendencias del mercado
                    self.update_market_trends(job_offer)
                    
            except Exception as e:
                logger.error(f"Error scraping Tecnoempleo page {page}: {str(e)}")
        
        return jobs
    
    def get_job_details(self, url):
        """Obtiene detalles adicionales de la oferta de trabajo"""
        details = {
            'description': '',
            'publication_date': datetime.date.today(),
            'salary_min': None,
            'salary_max': None,
            'applicants_count': 0,
            'skills': []
        }
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer descripción
            description_elem = soup.select_one('.job-description')
            if description_elem:
                details['description'] = description_elem.text.strip()
                
                # Extraer habilidades del texto
                details['skills'] = self.extract_skills_from_text(details['description'])
            
            # Extraer fecha de publicación
            date_elem = soup.select_one('.job-date')
            if date_elem:
                date_text = date_elem.text.strip()
                try:
                    # Parsear fecha (formato depende del sitio)
                    # Ejemplo simplificado
                    details['publication_date'] = datetime.datetime.strptime(date_text, '%d/%m/%Y').date()
                except:
                    pass
            
            # Extraer salario
            salary_elem = soup.select_one('.job-salary')
            if salary_elem:
                salary_text = salary_elem.text.strip()
                # Parsear salario (formato depende del sitio)
                # Ejemplo simplificado
                if '-' in salary_text:
                    try:
                        min_str, max_str = salary_text.split('-')
                        details['salary_min'] = float(min_str.replace('€', '').replace('.', '').strip())
                        details['salary_max'] = float(max_str.replace('€', '').replace('.', '').strip())
                    except:
                        pass
            
            # Extraer número de aplicantes (si está disponible)
            applicants_elem = soup.select_one('.job-applicants')
            if applicants_elem:
                try:
                    details['applicants_count'] = int(applicants_elem.text.strip().split()[0])
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Error getting job details from {url}: {str(e)}")
        
        return details
    
    def update_market_trends(self, job_offer):
        """Actualiza las tendencias del mercado basadas en la oferta"""
        today = datetime.date.today()
        
        for skill in job_offer.skills_required.all():
            trend, created = MarketTrend.objects.get_or_create(
                skill=skill,
                source=self.source,
                date=today,
                defaults={'demand_count': 1, 'worker_interest': job_offer.applicants_count}
            )
            
            if not created:
                trend.demand_count += 1
                trend.worker_interest += job_offer.applicants_count
                trend.save()

# Implementaciones similares para InfoJobs y LinkedIn
# ...
