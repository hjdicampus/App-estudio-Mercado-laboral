from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('gestor', 'Gestor de Proyectos'),
            ('colaborador', 'Colaborador'),
        ],
        default='colaborador',
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username