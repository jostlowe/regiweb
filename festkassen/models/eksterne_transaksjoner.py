from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .varer import Vare


class Bar(models.Model):
    gjengnavn = models.CharField(max_length=100)
    barnavn = models.CharField(max_length=100, blank=True, null=True)
    aktiv = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Barer"

    def __str__(self):
        if self.barnavn:
            return "%s (%s)" % (self.gjengnavn, self.barnavn)
        elif self.gjengnavn:
            return self.gjengnavn
        else:
            return "Ukjent Bar"


class BSF(models.Model):
    beskrivelse = models.CharField(max_length=200, blank=True, null=True)
    dato = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "BSFer"

    def __str__(self):
        return str(self.beskrivelse)


# Modeller for ekstern kryssing på Regi-hybel


class Eksternkrysseliste(models.Model):
    dato = models.DateTimeField(default=timezone.now)
    opprettet_av = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    bsf = models.ForeignKey(BSF, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Eksternkrysselister"

    def __str__(self):
        return "%s (%s)" % (self.bar, self.dato.date())


class EksternDranker(models.Model):
    navn = models.CharField(max_length=100)
    bartilhorighet = models.ForeignKey(Bar, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Eksterne drankere"

    def __str__(self):
        return self.navn


class EksternTransaksjon(models.Model):
    person = models.ForeignKey(EksternDranker, on_delete=models.CASCADE)
    tidsstempel = models.DateTimeField(default=timezone.now)
    vare = models.ForeignKey(Vare, on_delete=models.CASCADE)
    antall = models.PositiveIntegerField(default=0)
    stykkpris = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    eksternkrysseliste = models.ForeignKey(Eksternkrysseliste, on_delete=models.CASCADE)

    def sum(self):
        return self.stykkpris * self.antall

    class Meta:
        verbose_name_plural = "Eksterntransaksjoner"

    def __str__(self):
        return "%08d" % self.pk


# Transasksjonsmodeller
