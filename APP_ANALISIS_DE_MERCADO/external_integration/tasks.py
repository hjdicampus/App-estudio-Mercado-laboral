# external_integration/tasks.py

from .scrapers import TecnoempleoScraper, InfoJobsScraper, LinkedInScraper
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def update_job_market_data():
    """Tarea programada para actualizar datos del mercado laboral"""
    logger.info(f"Iniciando actualización de datos del mercado laboral: {timezone.now()}")
    
    # Tecnoempleo
    try:
        tecnoempleo_scraper = TecnoempleoScraper()
        tecnoempleo_jobs = tecnoempleo_scraper.scrape_jobs(pages=3)
        logger.info(f"Actualizadas {len(tecnoempleo_jobs)} ofertas de Tecnoempleo")
    except Exception as e:
        logger.error(f"Error actualizando datos de Tecnoempleo: {str(e)}")
    
    # InfoJobs
    try:
        infojobs_scraper = InfoJobsScraper()
        infojobs_jobs = infojobs_scraper.scrape_jobs(pages=3)
        logger.info(f"Actualizadas {len(infojobs_jobs)} ofertas de InfoJobs")
    except Exception as e:
        logger.error(f"Error actualizando datos de InfoJobs: {str(e)}")
    
    # LinkedIn
    try:
        linkedin_scraper = LinkedInScraper()
        linkedin_jobs = linkedin_scraper.scrape_jobs(pages=3)
        logger.info(f"Actualizadas {len(linkedin_jobs)} ofertas de LinkedIn")
    except Exception as e:
        logger.error(f"Error actualizando datos de LinkedIn: {str(e)}")
    
    logger.info(f"Finalizada actualización de datos del mercado laboral: {timezone.now()}")
