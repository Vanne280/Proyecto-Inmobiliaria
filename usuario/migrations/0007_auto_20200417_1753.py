# Generated by Django 2.2.10 on 2020-04-17 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_auto_20200417_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'permissions': (('agregar_inmueble', 'Puede agregar inmueble'), ('listar_inmueble', 'Puede listar inmueble'), ('editar_inmueble', 'Puede editar inmueble'), ('eliminar_inmueble', 'Puede eliminar inmueble'), ('gestionar_inmueble_propietario', 'Puede gestionar inmuebles y propietarios'), ('listar_propiedad_cliente', 'Puede listar inmuebles y propietarios'), ('editar_propiedad_cliente', 'Puede editar inmuebles y propietarios'), ('eliminar_propiedad_cliente', 'Puede eliminar inmuebles y propietarios'), ('ver_inmuebles', 'Puede ver inmuebles registrados'))},
        ),
    ]
