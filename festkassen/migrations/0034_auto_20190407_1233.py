# Generated by Django 2.1.7 on 2019-04-07 12:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('festkassen', '0033_bsf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bsf',
            name='dato',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
