from django.db import models


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

