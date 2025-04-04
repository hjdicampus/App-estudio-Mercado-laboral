# job_market/models.py

from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class JobSource(models.Model):
    TECNOEMPLEO = 'tecnoempleo'
    INFOJOBS = 'infojobs'
    LINKEDIN = 'linkedin'
    
    SOURCE_CHOICES = [
        (TECNOEMPLEO, 'Tecnoempleo'),
        (INFOJOBS, 'InfoJobs'),
        (LINKEDIN, 'LinkedIn'),
    ]
    
    name = models.CharField(max_length=20, choices=SOURCE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class JobOffer(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    publication_date = models.DateField()
    extraction_date = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(JobSource, on_delete=models.CASCADE)
    skills_required = models.ManyToManyField(Skill, related_name='job_offers')
    applicants_count = models.IntegerField(default=0)  # Número de personas que se han apuntado
    
    def __str__(self):
        return f"{self.title} - {self.company}"

class MarketTrend(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    source = models.ForeignKey(JobSource, on_delete=models.CASCADE)
    date = models.DateField()
    demand_count = models.IntegerField()  # Número de ofertas que piden esta habilidad
    worker_interest = models.IntegerField(default=0)  # Interés de los trabajadores (basado en aplicaciones)
    
    class Meta:
        unique_together = ('skill', 'source', 'date')
    
    def __str__(self):
        return f"{self.skill.name} - {self.source.name} - {self.date}"
