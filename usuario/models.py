from djongo import models
from django.contrib.auth.models import User


class Rol(models.Model):
    """ Crea un modelo con el nombre Rol y un campo llamado nombre """

    nombre = models.CharField(max_length=20)

    # Muestra correctamente el nombre del Rol en el admin de Django
    def __str__(self):
        return self.nombre

#Se crea clase Perfil
class Perfil(models.Model):
    """ Crea un modelo con el nombre Perfil, un campo llamado IDUser con relación
    uno a uno a la tabla User proporcionada por Django y otro campo llamado IDRol
    con llave foránea de la tabla Rol """

    IDUser = models.OneToOneField(User, on_delete = models.PROTECT)
    IDRol = models.ForeignKey(Rol, on_delete = models.PROTECT)
