from djongo import models


class Tipo_de_inmueble(models.Model):
    nombre = models.CharField(max_length=25, null=False)

    """
    Crea un modelo con el nombre Tipo_de_inmueble y un campo
    llamado nombre de tipo Varchar(25) y nulo
    """

    def __str__(self):
        return self.nombre
    """
    Función que muestracorrectamente el nombre del tipo de inmueble
    en el admin de Django
    """

class Tipo_de_oferta(models.Model):
    nombre = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=80, null=False)
    IDDepartamento = models.ForeignKey(Departamento, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    nombre = models.CharField(max_length=80, null=False)
    IDCiudad = models.ForeignKey(Ciudad, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    direccion = models.CharField(max_length=100, null=False)
    IDBarrio = models.ForeignKey(Barrio, null=False, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=9, decimal_places=0,  null=False)
    IDTipo_de_inmueble = models.ForeignKey(Tipo_de_inmueble, null=False, on_delete=models.PROTECT)
    IDTipo_de_oferta = models.ForeignKey(Tipo_de_oferta, null=False, on_delete=models.PROTECT)
    alcoba = models.IntegerField(null=False)
    baño = models.IntegerField(null=False)
    parqueadero = models.BooleanField(null=False)
    disponible = models.BooleanField(null=False)

class Imagenes(models.Model):
    ruta = models.FileField(null=True, upload_to="archivos/%Y/%m/%d")
    IDInmueble = models.ForeignKey(Inmueble, null=True, on_delete=models.PROTECT)
