from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from ..models import Innskudd, Krysseliste
from .admin import er_festkasse


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


