# Generated by Django 2.1.7 on 2019-04-07 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festkassen', '0040_auto_20190407_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eksterndranker',
            name='bartilhorighet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festkassen.Bar'),
        ),
    ]
