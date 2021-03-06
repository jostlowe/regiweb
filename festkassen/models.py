from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import itertools


class Vare(models.Model):
    navn = models.CharField(max_length=50)
    beskrivelse = models.CharField(max_length=200, null=True, blank=True)
    standardpris = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    prioritet = models.IntegerField(default=10,
                                    help_text= """
                                    Bestemmer hvilken kolonne varen skal stå i på en liste
                                    En lavere verdi vil putte varen lengre til venstre
                                    på en liste
                                    """)
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
        innskudd = Innskudd.objects.filter(festkassekonto=self).filter(godkjent=True)

        transaksjoner = itertools.chain(kryss, innskudd)
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


class Bar(models.Model):
    gjengnavn = models.CharField(max_length=100)
    barnavn = models.CharField(max_length=100, blank=True, null=True)
    aktiv = models.BooleanField(default=True)
    varer_paa_listene = models.ManyToManyField(Vare)

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
    dato = models.DateField(default=timezone.now)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    bsf = models.ForeignKey(BSF, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Eksternkrysselister"

    def __str__(self):
        return "%s (%s)" % (self.bar, self.dato)


class EksternDranker(models.Model):
    navn = models.CharField(max_length=100)
    kallenavn = models.CharField(max_length=100, null=True, blank=True, default="")
    bartilhorighet = models.ForeignKey(Bar, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Eksterne drankere"

    def __str__(self):
        if self.kallenavn:
            return "%s (%s)" % (self.navn, self.kallenavn)
        else:
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
    listedato = models.DateField(default=timezone.now)
    opprettet_av = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Krysselistetype, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Krysselister"

    def __str__(self):
        return "%s (%s)" % (self.type, str(self.listedato))


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
        if self.vare.er_additiv:
            return self.antall*self.stykkpris
        else:
            return -self.antall*self.stykkpris

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


