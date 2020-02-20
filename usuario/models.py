from djongo import models
from django.contrib.auth.models import User

#Se crea modelo de ROL
class Rol(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

#Se crea clase Perfil
class Perfil(models.Model):
    IDUser = models.OneToOneField(User, on_delete = models.PROTECT)
    IDRol = models.ForeignKey(Rol, on_delete = models.PROTECT)

    # def __str__(self):
    #     return self.per_user
