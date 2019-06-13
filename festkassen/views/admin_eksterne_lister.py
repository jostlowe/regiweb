from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms

from ..models import BSF, Eksternkrysseliste, EksternTransaksjon
from .admin import er_festkasse


class NyEksternlisteSkjema(forms.ModelForm):
    class Meta:
        model = Eksternkrysseliste
        fields = ('bar', 'bsf')
        widgets = {
            'dato': forms.DateInput(attrs={'type': 'date'})
        }


@login_required
@user_passes_test(er_festkasse)
def admin_rediger_ekstern_liste(request, bsf_pk, liste_pk):

    kryss = EksternTransaksjon.objects.filter(eksternkrysseliste=liste_pk)
    bsf = BSF.objects.get(pk=bsf_pk)
    eksternliste = Eksternkrysseliste.objects.get(pk=liste_pk)

    context = {
        'kryss': kryss,
        'bsf': bsf,
        'eksternliste': eksternliste,
    }

    if request.method == 'POST':
        nyEksternlisteSkjema = NyEksternlisteSkjema(request.POST)
        if nyEksternlisteSkjema.is_valid():
            nyEksternliste = Eksternkrysseliste(
                dato=nyEksternlisteSkjema.cleaned_data['dato'],
                bar=nyEksternlisteSkjema.cleaned_data['bar'],
                bsf=bsf_pk,
            )
            nyEksternliste.save()
            tilbakemelding = "Ny BSF registrert: %s" % (
                nyEksternliste,
            )
            context.update({
                'tilbakemelding': tilbakemelding
            })

    return render(request, 'festkassen/admin_rediger_ekstern_liste.html', context)

