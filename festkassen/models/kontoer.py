from django.db import models
from django.contrib.auth.models import User
import itertools


class Festkassekontotype(models.Model):
    navn = models.CharField(max_length=100)
    svartegrense = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        verbose_name_plural = "Festkassekontotyper"

    def __str__(self):
        return self.navn


class Festkassekonto(models.Model):
    regiweb_bruker = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Regiweb-brukeren som denne feskassekontoen skal asossieres med",
        blank=True,
        null=True
    )
    kontotype = models.ForeignKey(
        Festkassekontotype,
        on_delete=models.CASCADE,
    )
    aktiv = models.BooleanField(
        default=True,
        verbose_name="Aktiv konto",
        help_text="Markerer om festkassebrukeren er aktiv. Kryss av her heller enn å slette brukeren"
    )

    def saldo(self):
        kryss = Kryss.objects.filter(festkassekonto=self)
        bsf_regninger = BSFregning.objects.filter(festkassekonto=self)
        innskudd = Innskudd.objects.filter(festkassekonto=self).filter(godkjent=True)

        transaksjoner = itertools.chain(kryss, bsf_regninger, innskudd)
        saldo = sum([transaksjon.sum() for transaksjon in transaksjoner])
        return saldo

    class Meta:
        verbose_name_plural = "Festkassekontoer"

    def __str__(self):
        if self.regiweb_bruker:
            bruker = self.regiweb_bruker.username
            fullt_navn = self.regiweb_bruker.get_full_name()
            return "%s (%s)" % (fullt_navn, bruker)
        else:
            return "Uassosiert festkassekonto"

