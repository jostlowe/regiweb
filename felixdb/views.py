from django.shortcuts import render
from .models import Verv, Regifant, Vervperiode, Uke, Ukeverv, Ukevervperiode
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    regifanter = Regifant.objects.all()
    context = {
        "regifanter": regifanter
    }
    return render(request, 'felixdb/index.html', context)


def regifant(request, regifant_id):
    regifant = Regifant.objects.get(pk=regifant_id)
    vervperiodeliste = Vervperiode.objects.filter(regifant=regifant).order_by('-aar')
    ukevervperiodeliste = Ukevervperiode.objects.filter(regifant=regifant)
    context={
        "regifant": regifant,
        "vervperiodeliste": vervperiodeliste,
        "ukevervperiodeliste": ukevervperiodeliste
    }
    return render(request, 'felixdb/regifant.html', context)


def verv(request):
    vervliste = Verv.objects.order_by('navn')
    context = {'vervliste': vervliste}
    return render(request, 'felixdb/verv.html', context)


def vervdetalj(request, verv_id):
    verv = Verv.objects.get(pk=verv_id)
    vervperioder = Vervperiode.objects.filter(verv=verv)
    context = {
        'verv': verv,
        'vervperioder': vervperioder,
    }
    return render(request, 'felixdb/vervdetalj.html', context)


def ukeverv(request):
    ukevervliste = Ukeverv.objects.all()
    context = {
        'ukevervliste': ukevervliste
    }
    return render(request, 'felixdb/ukeverv.html', context)


def ukevervdetalj(request, ukeverv_id):
    ukeverv = Ukeverv.objects.get(pk=ukeverv_id)
    ukevervperioder = Ukevervperiode.objects.filter(ukeverv=ukeverv)
    context = {
        'ukeverv': ukeverv,
        'ukevervperioder': ukevervperioder,
    }
    return render(request, 'felixdb/ukevervdetalj.html', context)


def aarsoversikt(request, aar):
    vervperiodeliste = Vervperiode.objects.filter(aar=aar).order_by('-aar')
    context={
        "aar": aar,
        "vervperiodeliste": vervperiodeliste
    }
    return render(request, 'felixdb/aarsoversikt.html', context)


def uker(request):
    uker = Uke.objects.all().order_by('-aar')
    context = {
        'uker': uker
    }
    return render(request, 'felixdb/uker.html', context)


def ukedetalj(request, ukeaar):
    uke = Uke.objects.get(aar=ukeaar)
    ukevervperioder = Ukevervperiode.objects.filter(uke=uke)
    context = {
        'uke': uke,
        'ukevervperioder': ukevervperioder
    }
    return render(request, 'felixdb/ukedetalj.html', context)
