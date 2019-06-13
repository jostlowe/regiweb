from django.shortcuts import render
from ..models import Festkassekonto, Innskudd, Krysseliste
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django import forms


def har_brukeren_festkassekonto(user):
    return Festkassekonto.objects.filter(regiweb_bruker=user).exists()


def er_festkasse(user):
    return user.groups.filter(name='Festkasse').exists()


@login_required
@user_passes_test(er_festkasse)
def admin(request):
    context = {}
    return render(request, 'festkassen/admin.html', context)



