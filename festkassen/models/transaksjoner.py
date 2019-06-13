from django.db import models
from django.utils import timezone

from .eksterne_transaksjoner import BSF, Bar
from .interne_krysselister import Krysseliste, Krysselistetype
from .kontoer import Festkassekonto
from .varer import Vare


class Transaksjon(models.Model):
    tidsstempel = models.DateTimeField(default=timezone.now)
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    kommentar = models.CharField(max_length=200, blank=True, null=True)

    def sum(self):
        raise NotImplementedError

    class Meta:
        abstract = True

    def __str__(self):
        return "%08d" % self.pk


class Kryss(Transaksjon):
    vare = models.ForeignKey(Vare, on_delete=models.CASCADE)
    antall = models.PositiveIntegerField()
    stykkpris = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    krysseliste = models.ForeignKey(Krysseliste, on_delete=models.CASCADE)

    def sum(self):
        return self.antall*self.stykkpris

    class Meta:
        verbose_name_plural = "Kryss"


class BSFregning(Transaksjon):
    bsf = models.ForeignKey(BSF, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    belop = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def sum(self):
        return self.belop

    class Meta:
        verbose_name_plural = "BSF-regninger"
        verbose_name = "BSF-regning"


class Innskudd(Transaksjon):
    belop = models.DecimalField(max_digits=9, decimal_places=2)
    godkjent = models.BooleanField(default=False)
    er_utlegg = models.BooleanField(default=False)

    def sum(self):
        return self.belop

    class Meta:
        verbose_name_plural = "Innskudd"
