from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms

from ..models import BSF, Eksternkrysseliste
from .admin import er_festkasse


class NyBsfSkjema(forms.ModelForm):
    class Meta:
        model = BSF
        fields = ('beskrivelse', 'dato')
        widgets = {
            'dato': forms.DateInput(attrs={'type': 'date'})
        }


@login_required
@user_passes_test(er_festkasse)
def admin_bsfer(request):

    bsfer = BSF.objects.all().order_by('-dato')[:30]
    nybsfskjema = NyBsfSkjema()
    context = {
        'bsfer': bsfer,
        'nybsfskjema': nybsfskjema,
    }

    if request.method == 'POST':
        nybsfskjema = NyBsfSkjema(request.POST)
        if nybsfskjema.is_valid():
            ny_bsf = BSF(
                beskrivelse=nybsfskjema.cleaned_data['beskrivelse'],
                dato=nybsfskjema.cleaned_data['dato']
            )
            ny_bsf.save()
            tilbakemelding = "Ny BSF registrert: %s" % (
                ny_bsf,
            )
            context.update({
                'tilbakemelding': tilbakemelding
            })

    return render(request, 'festkassen/admin_bsfer.html', context)


@login_required
@user_passes_test(er_festkasse)
def admin_rediger_bsf(request, bsf_pk):
    eksternlister = Eksternkrysseliste.objects.filter(bsf=bsf_pk)
    bsf = BSF.objects.get(pk=bsf_pk)
    context = {
        'bsf': bsf,
        'eksternlister': eksternlister
    }
    return render(request, 'festkassen/admin_rediger_bsf.html', context)
