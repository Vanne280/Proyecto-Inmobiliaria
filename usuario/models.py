from djongo import models
from django.contrib.auth.models import User

#Se crea modelo de ROL
class Rol(models.Model):
    rol_nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.rol_nombre

#Se crea clase Perfil
class Perfil(models.Model):
    per_user = models.OneToOneField(User, on_delete = models.PROTECT)
    per_rol = models.ForeignKey(Rol, on_delete = models.PROTECT)

    # def __str__(self):
    #     return self.per_user
