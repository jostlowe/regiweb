from django.shortcuts import render
from .models import Festkassekonto, Innskudd, BSFregning, Kryss
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User, Group


def har_brukeren_festkassekonto(user):
    return Festkassekonto.objects.filter(regiweb_bruker=user).exists()


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


class Innskuddskjema(forms.Form):
    sum = forms.DecimalField(max_digits=9, decimal_places=2, min_value=0)
    kommentar = forms.CharField(max_length=200, required=False)


# ---------------------------------------------
# Festkasse-admin
# ---------------------------------------------

def er_festkasse(user):
    return user.groups.filter(name='Festkasse').exists()


@login_required
@user_passes_test(er_festkasse)
def admin(request):
    context = {}
    return render(request, 'festkassen/admin.html', context)


@login_required
@user_passes_test(er_festkasse)
def admin_innskudd(request):
    ventende_innskudd = Innskudd.objects.filter(godkjent=False).order_by('-tidsstempel')
    godkjente_innskudd = Innskudd.objects.filter(godkjent=True).order_by('-tidsstempel')[:30]
    context = {
        'ventende_innskudd': ventende_innskudd,
        'godkjente_innskudd': godkjente_innskudd,
    }
    return render(request, 'festkassen/admin_innskudd.html', context)


@login_required
@user_passes_test(er_festkasse)
def admin_godkjenn_innskudd(request, innskudd_pk):
    godkjent_innskudd = Innskudd.objects.get(pk=innskudd_pk)
    godkjent_innskudd.godkjent = True
    godkjent_innskudd.save()

    return HttpResponseRedirect(reverse('festkassen:admin_innskudd'))
