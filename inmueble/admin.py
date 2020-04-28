from django.contrib import admin
from .models import (Tipo_de_inmueble, Tipo_de_oferta, Departamento,
                    Ciudad, Barrio, Inmueble, Imagenes,
                    Propietarios_arrendatarios, cita)

# Register your models here.
admin.site.register(Tipo_de_inmueble)
admin.site.register(Tipo_de_oferta)
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Barrio)
admin.site.register(Inmueble)
admin.site.register(Imagenes)
admin.site.register(Propietarios_arrendatarios)
admin.site.register(cita)
