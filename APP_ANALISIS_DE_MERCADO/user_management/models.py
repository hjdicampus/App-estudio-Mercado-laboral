# user_management/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    PROJECT_MANAGER = 'project_manager'
    COLLABORATOR = 'collaborator'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (PROJECT_MANAGER, 'Gestor de Proyectos'),
        (COLLABORATOR, 'Colaborador'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=COLLABORATOR)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Habilidades del usuario (relación muchos a muchos)
    skills = models.ManyToManyField('job_market.Skill', blank=True)
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_project_manager(self):
        return self.role == self.PROJECT_MANAGER
    
    def is_collaborator(self):
        return self.role == self.COLLABORATOR
