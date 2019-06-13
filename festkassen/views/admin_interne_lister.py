from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms

from ..models import Festkassekonto, Kryss, Krysseliste, Vare
from .admin import er_festkasse


class NyKrysselisteSkjema(forms.ModelForm):
    class Meta:
        model = Krysseliste
        fields = ('listedato', 'type')
        widgets = {
            'listedato': forms.DateInput(attrs={'type': 'date'})
        }


@login_required
@user_passes_test(er_festkasse)
def admin_interne_krysselister(request):

    krysselister = Krysseliste.objects.all().order_by('-listedato')[:30]
    nykrysselisteskjema = NyKrysselisteSkjema()
    context = {
        'krysselister': krysselister,
        'nykrysselisteskjema': nykrysselisteskjema,
    }

    if request.method == 'POST':
        nykrysselisteskjema = NyKrysselisteSkjema(request.POST)
        if nykrysselisteskjema.is_valid():
            ny_krysseliste = Krysseliste(
                listedato=nykrysselisteskjema.cleaned_data['listedato'],
                type=nykrysselisteskjema.cleaned_data['type'],
                opprettet_av=request.user,
            )
            ny_krysseliste.save()
            tilbakemelding = "Ny krysseliste registrert: %s" % (
                ny_krysseliste,
            )
            context.update({
                'tilbakemelding': tilbakemelding
            })

    return render(request, 'festkassen/admin_interne_krysselister.html', context)


@login_required
@user_passes_test(er_festkasse)
def admin_rediger_krysseliste(request, krysseliste_pk):
    kryss = Kryss.objects.filter(krysseliste=krysseliste_pk)
    krysseliste = Krysseliste.objects.get(pk=krysseliste_pk)
    kontoer = krysseliste.type.festkassekontoer_paa_lista.all()
    varer = krysseliste.type.varer.all()
    varenavn = [vare.navn for vare in varer]

    context = {
        'kryss': kryss,
        'krysseliste': krysseliste,
        'varer': varer,
        'kontoer': kontoer
    }

    if request.method == "POST":
        konto = Festkassekonto.objects.get(pk=int(request.POST['konto']))

        # Filtrerer ut alle key-value-par i request.POST som ikke er gyldige varer,
        # og sørger for at alle kryss er heltall og ikke strings
        # Det finnes garantert en bedre måte å gjøre dette på :P
        nye_kryss = {vare: int(request.POST[vare]) for vare in varenavn if int(request.POST[vare]) > 0}

        for navn in nye_kryss:
            vare = Vare.objects.get(navn=navn)
            nytt_kryss = Kryss(
                festkassekonto=konto,
                vare=vare,
                antall=nye_kryss[navn],
                stykkpris=vare.standardpris,
                krysseliste=krysseliste
            )
            nytt_kryss.save()

    return render(request, 'festkassen/admin_rediger_krysseliste.html', context)


@login_required
@user_passes_test(er_festkasse)
def admin_slett_kryss(request, krysseliste_pk, kryss_pk):
    Kryss.objects.get(pk=kryss_pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


