from django.shortcuts import render
from .models import Festkassekonto, Innskudd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms


@login_required
def forside(request):

    if not har_brukeren_festkassekonto(request):
        return render(request, 'festkassen/ingen_festkassekonto.html', {})

    context = {}
    return render(request, 'festkassen/forside.html', context)


@login_required
def innskudd(request):

    if not har_brukeren_festkassekonto(request):
        return render(request, 'festkassen/ingen_festkassekonto.html', {})

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


def har_brukeren_festkassekonto(request):
    festkassekonto = Festkassekonto.objects.filter(regiweb_bruker=request.user).first()
    if festkassekonto:
        return True
    return False


class Innskuddskjema(forms.Form):
    sum = forms.DecimalField(max_digits=9, decimal_places=2, min_value=0)
    kommentar = forms.CharField(max_length=200, required=False)
