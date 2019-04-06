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
    standardpris = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    er_additiv = models.BooleanField(
        default=False,
        verbose_name="Er additiv",
        help_text="""Hvis denne boksen er krysset av 
            vil prisen av varen LEGGES TIL festkassekontoens saldo.
            Dersom den ikke er krysset av vil prisen TREKKES FRA
            festkassekontoens saldo"""
    )

    class Meta:
        verbose_name_plural = "Varer"

    def __str__(self):
        return self.navn


class Transaksjon(models.Model):
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    tidsstempel = models.DateTimeField(default=timezone.now)
    antall = models.PositiveIntegerField(default=0)
    stykkpris = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    vare = models.ForeignKey(Vare, on_delete=models.CASCADE, null=True, blank=True)

    godkjent = models.BooleanField(
        default=False,
        verbose_name="Godkjent av festkasse",
        help_text="""Krysses av for å godkjenne varer, som f.eks. 
            innskudd på festkassen eller utlegg"""
    )

    def sum(self):
        return self.stykkpris * self.antall

    class Meta:
        verbose_name_plural = "Transaksjoner"

    def __str__(self):
        return "%08d" % self.pk


