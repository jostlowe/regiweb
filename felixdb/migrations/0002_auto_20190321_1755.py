# Generated by Django 2.1.7 on 2019-03-21 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('felixdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regifant',
            options={'verbose_name_plural': 'Regifanter'},
        ),
        migrations.AlterModelOptions(
            name='verv',
            options={'verbose_name_plural': 'Verv'},
        ),
        migrations.AlterField(
            model_name='regifant',
            name='adresse',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='doed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='dtp_kommandor',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='dtp_ridder',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='fasttelefon',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='foedt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='hjemmeadresse',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='hjemmepostnr',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='hjemmepoststed',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='hjemmetelefon',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='jobb',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='kallenavn',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='livsvarig_medlem',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='merknad',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='mobil',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='pensjonert',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='postnr',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='poststed',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='skole',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='regifant',
            name='tatt_opp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
