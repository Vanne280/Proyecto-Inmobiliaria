# Generated by Django 2.2.10 on 2020-04-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0017_remove_inmueble_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='imagenppal',
            field=models.FileField(default=1, upload_to='imagenes/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
