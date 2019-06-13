from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms

from ..models import Festkassekonto, Innskudd, BSFregning, Kryss
from .admin import har_brukeren_festkassekonto


class Innskuddskjema(forms.Form):
    sum = forms.DecimalField(max_digits=9, decimal_places=2, min_value=0)
    kommentar = forms.CharField(max_length=200, required=False)


@login_required
@user_passes_test(har_brukeren_festkassekonto)
def forside(request):

    # Hent transaksjonsdata fra festkassens backend
    festkassekonto = Festkassekonto.objects.get(regiweb_bruker=request.user)
    innskudd = Innskudd.objects.filter(festkassekonto=festkassekonto).order_by('-tidsstempel')
    bsf_regninger = BSFregning.objects.filter(festkassekonto=festkassekonto).order_by('-tidsstempel')
    kryss = Kryss.objects.filter(festkassekonto=festkassekonto).order_by('-tidsstempel')
    saldo = festkassekonto.saldo()

    context = {
        'innskudd': innskudd,
        'bsf_regninger': bsf_regninger,
        'kryss': kryss,
        'saldo': saldo
    }

    return render(request, 'festkassen/forside.html', context)


@login_required
@user_passes_test(har_brukeren_festkassekonto)
def innskudd(request):

    festkassekonto = Festkassekonto.objects.filter(regiweb_bruker=request.user).first()
    innskuddskjema = Innskuddskjema()
    context = {
        'festkassekonto': festkassekonto,
        'innskuddskjema': innskuddskjema
    }

    if request.method == 'POST':
        innskuddskjema = Innskuddskjema(request.POST)
        if innskuddskjema.is_valid():
            nytt_innskudd = Innskudd(
                belop=innskuddskjema.cleaned_data['sum'],
                kommentar=innskuddskjema.cleaned_data['kommentar'],
                festkassekonto=festkassekonto
            )
            nytt_innskudd.save()
            tilbakemelding = "innskudd på %s registrert på %s med ID %s" % (
                nytt_innskudd.belop,
                festkassekonto.regiweb_bruker.get_full_name(),
                nytt_innskudd.pk,
            )
            context.update({
                'tilbakemelding': tilbakemelding
            })

    return render(request, 'festkassen/innskudd.html', context)
