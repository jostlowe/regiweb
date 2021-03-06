from django.db import models
# Create your models here.

class Regifant(models.Model):

    # personalia
    fornavn = models.CharField(max_length=100)
    etternavn = models.CharField(max_length=100)
    kallenavn = models.CharField(max_length=100, blank=True)

    # Regi-info
    er_aktiv = models.BooleanField(default=True)

    # Tid og datoer
    foedt = models.IntegerField(blank=True, null=True)
    doed = models.IntegerField(blank=True, null=True)
    tatt_opp = models.IntegerField(blank=True, null=True)
    pensjonert = models.IntegerField(blank=True, null=True)

    # Kontaktinfo
    mobil = models.CharField(max_length=100, blank=True)
    fasttelefon = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=100, blank=True)
    postnr = models.CharField(max_length=100, blank=True)
    poststed = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    hjemmeadresse = models.CharField(max_length=100, blank=True)
    hjemmepostnr = models.CharField(max_length=100, blank=True)
    hjemmepoststed = models.CharField(max_length=100, blank=True)
    hjemmetelefon = models.CharField(max_length=100, blank=True)

    # Jobb og Utdanning
    jobb = models.CharField(max_length=100, blank=True)
    skole = models.CharField(max_length=100, blank=True)
    merknad = models.CharField(max_length=100, blank=True)

    # Utmerkelser
    dtp_ridder = models.IntegerField(blank=True, null=True)
    dtp_kommandor = models.IntegerField(blank=True, null=True)
    livsvarig_medlem = models.IntegerField(blank=True, null=True)
    mf58 = models.BooleanField()

    # Annet
    bilde = models.ImageField(blank=True, null=True)

    def navn(self):
        return self.fornavn + " " + self.etternavn

    def __str__(self):
        return self.navn()

    class Meta:
        verbose_name_plural = "Regifanter"


class Verv(models.Model):

    navn = models.CharField(max_length=100)
    prioritet = models.IntegerField()
    kort_beskrivelse = models.CharField(max_length=500)

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name_plural = "Verv"

    '''
    @staticmethod
    def parse_from_csv():
        import csv
        with open("verv.csv", 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                id, navn, pri, besk = line
                q = Verv(navn=navn, prioritet=pri, kort_beskrivelse=besk)
                q.save()
    '''


class Vervperiode(models.Model):
    verv = models.ForeignKey(Verv, on_delete=models.CASCADE)
    regifant = models.ForeignKey(Regifant, on_delete=models.CASCADE)
    aar = models.IntegerField()

    class Meta:
        verbose_name_plural = "Vervperioder"

    def __str__(self):
        return "%s - %s (%i)" % (self.regifant.navn(), self.verv.navn, self.aar)


class Uke(models.Model):
    ukenavn = models.CharField(max_length=100)
    aar = models.IntegerField()

    class Meta:
        verbose_name_plural = "Uker"

    def __str__(self):
        return self.ukenavn + " (" + str(self.aar) + ")"


class Ukeverv(models.Model):

    navn = models.CharField(max_length=100)
    kort_beskrivelse = models.CharField(max_length=500)

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name_plural = "Ukeverv"


class Ukevervperiode(models.Model):
    ukeverv = models.ForeignKey(Ukeverv, on_delete=models.CASCADE)
    regifant = models.ForeignKey(Regifant, on_delete=models.CASCADE)
    uke = models.ForeignKey(Uke, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Ukevervperioder"

    def __str__(self):
        return "%s - %s (%s)" % (self.regifant.navn(), self.ukeverv.navn, self.uke)

