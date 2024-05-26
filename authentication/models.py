from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    CREATOR = 'CREATOR'
    ADMIN = 'ADMIN'


    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (ADMIN, 'Administrateur'),
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')