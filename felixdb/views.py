from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Verv, Regifant, Vervperiode


def verv(request):
    vervliste = Verv.objects.order_by('navn')
    context = {'vervliste': vervliste}
    return render(request, 'felixdb/verv.html', context)


def vervdetalj(request, verv_id):
    verv = Verv.objects.get(pk=verv_id)
    context = {'verv': verv}
    return render(request, 'felixdb/vervdetalj.html', context)


def index(request):
    regifanter = Regifant.objects.all()
    context = {
        "regifanter": regifanter
    }
    return render(request, 'felixdb/index.html', context)


def regifant(request, regifant_id):
    regifant = Regifant.objects.get(pk=regifant_id)
    vervperiodeliste = Vervperiode.objects.filter(regifant=regifant).order_by('-aar')
    context={
        "regifant": regifant,
        "vervperiodeliste": vervperiodeliste
    }
    return render(request, 'felixdb/regifant.html', context)


def aarsoversikt(request, aar):
    vervperiodeliste = Vervperiode.objects.filter(aar=aar).order_by('-aar')
    context={
        "aar": aar,
        "vervperiodeliste": vervperiodeliste
    }
    return render(request, 'felixdb/aarsoversikt.html', context)

# Create your views here.
