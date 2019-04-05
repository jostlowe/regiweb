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
        return sum([0 for transaksjon in transaksjoner])


    class Meta:
        verbose_name_plural = "Festkassekontoer"

    def __str__(self):
        if self.regiweb_bruker:
            bruker = self.regiweb_bruker.username
            fullt_navn = self.regiweb_bruker.get_full_name()
            return "%s (%s)" % (bruker, fullt_navn)
        else:
            return "Uassosiert festkassekonto"


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


class Vare(models.Model):
    navn = models.CharField(max_length=50)
    beskrivelse = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Varer"

    def __str__(self):
        return self.navn


class Varepris(models.Model):
    vare = models.ForeignKey(Vare, on_delete=models.CASCADE)
    pris = models.DecimalField(decimal_places=2, max_digits=7)
    gyldig_fra = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Varepriser"

    def __str__(self):
        return "%s (%s)" % (self.vare.navn, str(self.pris))


class Transaksjon(models.Model):
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    tidsstempel = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Transaksjoner"

    def __str__(self):
        return "%08d" % self.pk


