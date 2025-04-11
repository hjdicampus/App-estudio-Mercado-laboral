from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobOffer(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)  # Ahora es opcional
    skills = models.ManyToManyField(Skill, blank=True)
    salary = models.CharField(max_length=100, blank=True, null=True)    # También opcional
    date_posted = models.DateField()
    source = models.CharField(max_length=50)
    url = models.URLField(unique=True)

    def __str__(self):
        return f"{self.title} - {self.company}"