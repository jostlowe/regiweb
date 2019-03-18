from django.db import models
from django.utils import timezone

# Create your models here.


class Regifant(models.Model):

    # personalia
    fornavn = models.CharField(max_length=100)
    etternavn = models.CharField(max_length=100)
    kallenavn = models.CharField(max_length=100)

    # Tid og datoer
    aar_valg = [aar for aar in range(1850, timezone.now().year+1)]
    foedt = models.IntegerField(choices=aar_valg)
    doed = models.IntegerField(choices=aar_valg)
    tatt_opp = models.IntegerField(choices=aar_valg, default=timezone.now().year)
    pensjonert = models.IntegerField(choices=aar_valg)

    # Kontaktinfo
    mobil, fasttelefon = [models.CharField(max_length=100)]*2
    adresse, postnr, poststed = [models.CharField(max_length=100)]*3
    email = models.EmailField()
    hjemmeadresse, hjemmepostnr, hjemmepoststed, hjemmetelefon = [models.CharField(max_length=100)]*4

    # Jobb og Utdanning
    jobb, skole = [models.CharField(max_length=100)]*2
    merknad = models.CharField(max_length=100)

    # Utmerkelser
    dtp_ridder, dtp_kommandor = [models.IntegerField(choices=aar_valg)]*2
    livsvarig_medlem = models.IntegerField(choices=aar_valg)
    mf58 = models.BooleanField()

    # Annet
    bilde = models.ImageField()
