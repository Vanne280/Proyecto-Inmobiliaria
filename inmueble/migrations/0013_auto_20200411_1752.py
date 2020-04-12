# Generated by Django 2.2.10 on 2020-04-11 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inmueble', '0012_auto_20200408_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='descripcion',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.CreateModel(
            name='Propietarios_arrendatarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cliente', models.BooleanField()),
                ('inmueble', models.ManyToManyField(to='inmueble.Inmueble')),
                ('usuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.DateTimeField()),
                ('inmueble', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inmueble.Inmueble')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
