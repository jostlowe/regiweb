# Generated by Django 2.1.7 on 2019-04-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festkassen', '0026_auto_20190406_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='vare',
            name='standardpris',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
