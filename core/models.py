from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
