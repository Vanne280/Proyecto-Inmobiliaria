from django.db import models
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

    class Meta:
        """ Clase para introducir nuevas funcionalidades en la clase Perfil """

        permissions = (
                       # Permisos para asesores
                       ("agregar_inmueble", "Puede agregar inmueble"),
                       ("listar_inmueble", "Puede listar inmueble"),
                       ("editar_inmueble", "Puede editar inmueble"),
                       ("eliminar_inmueble", "Puede eliminar inmueble"),
                       ("gestionar_inmueble_propietario", "Puede gestionar inmuebles y propietarios"),
                       ("listar_propiedad_cliente", "Puede listar inmuebles y propietarios"),
                       ("editar_propiedad_cliente", "Puede editar inmuebles y propietarios"),
                       ("eliminar_propiedad_cliente", "Puede eliminar inmuebles y propietarios"),

                       # Permisos para clientes
                       ("ver_inmuebles", "Puede ver inmuebles registrados"),
                      )
