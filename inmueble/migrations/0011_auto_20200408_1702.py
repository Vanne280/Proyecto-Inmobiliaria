# Generated by Django 2.2.10 on 2020-04-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0010_inmueble_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='imagen',
            field=models.FileField(null=True, upload_to='imagenes/%Y/%m/%d'),
        ),
    ]
