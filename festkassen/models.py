from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
        transaksjoner = Transaksjon.objects.filter(festkassekonto=self)
        return sum([transaksjon.betegnet_sum() for transaksjon in transaksjoner])


    class Meta:
        verbose_name_plural = "Festkassekontoer"

    def __str__(self):
        if self.regiweb_bruker:
            bruker = self.regiweb_bruker.username
            fullt_navn = self.regiweb_bruker.get_full_name()
            return "%s (%s)" % (bruker, fullt_navn)
        else:
            return "Uassosiert festkassekonto"


class Transaksjonstype(models.Model):
    navn = models.CharField(max_length=100)
    beskrivelse = models.CharField(max_length=1000)
    er_additiv = models.BooleanField(
        default=False,
        help_text="""
            Dersom dette feltet er krysset av, 
            vil transaksjoner av denne typen LEGGE TIL
            penger på brukerens festkassekonto. Dersom feltet
            IKKE er krysset vil denne typen transaksjon TREKKE FRA
            penger fra brukerens festkassekonto
            """,
    )
    maa_godkjennes = models.BooleanField(
        default=False,
        verbose_name="Må godkjennes",
        help_text="""
            Kryss av dersom denne typen transaksjon må godkjennes
            av festkasse før den skal registreres i festkassen.
            eksempelvis, så burde "innskudd" og "utlegg" godkjennes av festkasse
        """,
    )

    class Meta:
        verbose_name_plural = "Transaksjonstyper"

    def __str__(self):
        return self.navn


class Bar(models.Model):
    gjengnavn = models.CharField(max_length=100)
    barnavn = models.CharField(max_length=100, blank=True, null=True)
    aktiv = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Barer"

    def __str__(self):
        if self.barnavn:
            return "%s (%s)" % (self.barnavn, self.gjengnavn)
        elif self.gjengnavn:
            return self.gjengnavn
        else:
            return "Ukjent Bar"


class Transaksjon(models.Model):
    transaksjonstype = models.ForeignKey(Transaksjonstype, on_delete=models.CASCADE)
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=7)
    tidsstempel = models.DateTimeField(default=timezone.now)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, null=True, blank=True)

    def betegnet_sum(self):
        if self.transaksjonstype.er_additiv:
            return self.sum
        else:
            return -self.sum

    class Meta:
        verbose_name_plural = "Transaksjoner"

    def __str__(self):
        return "%s (%s)" % (self.festkassekonto.regiweb_bruker.username, self.transaksjonstype)


