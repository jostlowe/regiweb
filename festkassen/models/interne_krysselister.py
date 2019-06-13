from django.db import models
from django.contrib.auth.models import User
from .varer import Vare
from .kontoer import Festkassekonto


class Krysselistetype(models.Model):
    navn = models.CharField(max_length=100)
    beskrivelse = models.CharField(max_length=200, blank=True, null=True)
    festkassekontoer_paa_lista = models.ManyToManyField(Festkassekonto)
    varer = models.ManyToManyField(Vare)

    class Meta:
        verbose_name_plural = "Krysselistetyper"

    def __str__(self):
        return self.navn


class Krysseliste(models.Model):
    listedato = models.DateField()
    opprettet_av = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Krysselistetype, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Krysselister"

    def __str__(self):
        return "%s (%s)" % (self.type, str(self.listedato))

