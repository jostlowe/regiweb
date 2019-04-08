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
            return "%s (%s)" % (self.gjengnavn, self.barnavn)
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


class Krysselistetype(models.Model):
    navn = models.CharField(max_length=100)
    beskrivelse = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Krysselistetyper"

    def __str__(self):
        return self.navn


class Krysseliste(models.Model):
    dato = models.DateTimeField(default=timezone.now)
    opprettet_av = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    type = models.ForeignKey(Krysselistetype, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Krysselister"

    def __str__(self):
        return "%s (%s)" % (self.type , str(self.dato.date()))


class Transaksjon(models.Model):
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    tidsstempel = models.DateTimeField(default=timezone.now)
    vare = models.ForeignKey(Vare, on_delete=models.CASCADE, null=True, blank=True)
    antall = models.PositiveIntegerField(default=0)
    stykkpris = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    godkjent = models.BooleanField(
        default=False,
        verbose_name="Godkjent av festkasse",
        help_text="""Krysses av for å godkjenne varer, som f.eks. 
            innskudd på festkassen eller utlegg"""
    )
    krysseliste = models.ForeignKey(Krysseliste, null=True, blank=True, on_delete=models.CASCADE)

    def sum(self):
        return self.stykkpris * self.antall

    class Meta:
        verbose_name_plural = "Transaksjoner"

    def __str__(self):
        return "%08d" % self.pk


class BSF(models.Model):
    beskrivelse = models.CharField(max_length=200, blank=True, null=True)
    dato = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "BSFer"

    def __str__(self):
        return str(self.beskrivelse)


class BSFRegning(models.Model):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    bsf = models.ForeignKey(BSF, on_delete=models.CASCADE)
    festkassekonto = models.ForeignKey(Festkassekonto, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=7, default=0)

    class Meta:
        verbose_name_plural = "BSF-regninger"
        verbose_name = "BSF-regning"

    def __str__(self):
        return "%s, %s (%s)" % (self.festkassekonto, self.bsf, self.bar)


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

