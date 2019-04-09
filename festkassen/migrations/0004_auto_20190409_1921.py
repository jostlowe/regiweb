# Generated by Django 2.1.7 on 2019-04-09 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festkassen', '0003_bsfregning_innskudd_kryss'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bsfregning',
            options={'verbose_name': 'BSF-regning', 'verbose_name_plural': 'BSF-regninger'},
        ),
        migrations.AlterModelOptions(
            name='innskudd',
            options={'verbose_name_plural': 'Innskudd'},
        ),
        migrations.AlterModelOptions(
            name='kryss',
            options={'verbose_name_plural': 'Kryss'},
        ),
        migrations.AlterField(
            model_name='krysseliste',
            name='opprettet_av',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='krysseliste',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festkassen.Krysselistetype'),
        ),
    ]
