from djongo import models
from django.contrib.auth.models import User


class Tipo_de_inmueble(models.Model):
    """ Crea un modelo con el nombre Tipo_de_inmueble y un campo llamado nombre """

    nombre = models.CharField(max_length=25, null=False)

    # Muestra correctamente el nombre del tipo de inmueble en el admin de Django
    def __str__(self):
        return self.nombre

class Tipo_de_oferta(models.Model):
    """ Crea un modelo con el nombre Tipo_de_oferta y un campo llamado nombre """

    nombre = models.CharField(max_length=20, null=False)

    # Muestra correctamente el nombre del tipo de oferta en el admin de Django
    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    """ Crea un modelo con el nombre Departamento y un campo llamado nombre """

    nombre = models.CharField(max_length=80, null=False)

    # Muestra correctamente el nombre del Departamento en el admin de Django
    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    """ Crea un modelo con el nombre Ciudad, un campo llamado nombre y otro campo
    llamado IDDepartamento con llave foránea de la tabla Departamento """

    nombre = models.CharField(max_length=80, null=False)
    IDDepartamento = models.ForeignKey(Departamento, null=False, on_delete=models.PROTECT)

    # Muestra correctamente el nombre de la Ciudad en el admin de Django
    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    """ Crea un modelo con el nombre Barrio, un campo llamado nombre y otro campo
    llamado IDCiudad con llave foránea de la tabla Ciudad """

    nombre = models.CharField(max_length=80, null=False)
    IDCiudad = models.ForeignKey(Ciudad, null=False, on_delete=models.PROTECT)

    # Muestra correctamente el nombre del Barrio en el admin de Django
    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    """ Crea un modelo con el nombre Inmueble con un campo direccion, un campo IDBarrio
        con llave foránea de la tabla Barrio, un campo precio, un campo IDTipo_de_inmueble
        con llave foránea de la tabla Tipo_de_inmueble, un campo IDTipo_de_oferta con llave
        foránea de la tabla Tipo_de_oferta, un campo alcoba, un campo baño, un campo parqueadero,
        un campo disponible, un campo descripcion y un campo imagen """

    direccion = models.CharField(max_length=100, null=False)
    IDBarrio = models.ForeignKey(Barrio, null=False, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=9, decimal_places=0,  null=False)
    IDTipo_de_inmueble = models.ForeignKey(Tipo_de_inmueble, null=False, on_delete=models.PROTECT)
    IDTipo_de_oferta = models.ForeignKey(Tipo_de_oferta, null=False, on_delete=models.PROTECT)
    alcoba = models.IntegerField(null=False)
    baño = models.IntegerField(null=False)
    parqueadero = models.BooleanField(null=False)
    disponible = models.BooleanField(null=False)
    descripcion = models.CharField(max_length=300, null=True)
    imagen = models.ImageField(null=True, upload_to="imagenes/%Y/%m/%d")

class Imagenes(models.Model):
    """ Crea un modelo con el nombre Imagenes con un campo ruta y un campo IDInmueble
        con llave foránea de la tabla Inmueble """

    ruta = models.ImageField(null=True, upload_to="imagenes/%Y/%m/%d")
    IDInmueble = models.ForeignKey(Inmueble, null=True, on_delete=models.PROTECT)

class Propietarios_arrendatarios(models.Model):
    """docstring for cita."""

    usuario = models.ManyToManyField(User)
    inmueble = models.ManyToManyField(Inmueble)
    tipo_cliente = models.BooleanField(null=False)

class Cita(models.Model):
    """docstring for cita."""

    inmueble = models.ForeignKey(Inmueble, null=False, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, null=False, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
