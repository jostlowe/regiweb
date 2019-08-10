from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Wikiside(models.Model):
    tittel = models.CharField(max_length=100)
    dato_opprettet = models.DateTimeField('Opprettet', auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tittel)
        super(Wikiside, self).save(*args, **kwargs)

    def __str__(self):
        return self.tittel

    class Meta:
        verbose_name_plural = "Wikisider"

    def get_absolute_url(self):
        return reverse('revisjon_create', kwargs={'pk': self.pk})


class Revisjon(models.Model):
    wikiside = models.ForeignKey(Wikiside, null=True, on_delete=models.CASCADE, related_name='revisjon')
    innhold = models.TextField('Innhold')
    forfatter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sist_endret = models.DateTimeField('Sist endret', auto_now=True)
    kommentar = models.TextField('Kommentar', blank=True)

    class Meta:
        verbose_name = 'Revisjon'
        verbose_name_plural = 'Revisjoner'
        ordering = ['-sist_endret']
        get_latest_by = ['sist_endret']

    def __str__(self):
        return self.innhold

    def get_absolute_url(self):
        return reverse('wikiside', kwargs={'pk': self.pk})