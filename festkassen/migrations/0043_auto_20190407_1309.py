# Generated by Django 2.1.7 on 2019-04-07 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festkassen', '0042_eksterntransaksjon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eksterntransaksjon',
            name='eksternkrysseliste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festkassen.Eksternkrysseliste'),
        ),
    ]
