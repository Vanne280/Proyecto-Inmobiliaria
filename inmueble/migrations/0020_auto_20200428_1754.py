# Generated by Django 2.2.10 on 2020-04-28 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0019_auto_20200428_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='telefono',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
