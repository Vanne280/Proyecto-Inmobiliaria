# Generated by Django 2.2.10 on 2020-04-23 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0016_auto_20200423_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmueble',
            name='imagen',
        ),
    ]
