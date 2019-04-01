from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from felixdb.models import Regifant
# Create your views here.

def index(request):
    context = {}
    return render(request, 'hjem/index.html', context)

def kontakt(request):
    aktive_regifanter = Regifant.objects.filter(er_aktiv=True)
    context = {'aktive_regifanter': aktive_regifanter}
    return render(request, 'hjem/kontakt.html', context)

def techspecs(request):
    context = {}
    return render(request, 'hjem/techspecs.html', context)

def om(request):
    context = {}
    return render(request, 'hjem/om.html', context)

@login_required
def intern(request):
    context = {}
    return render(request, 'hjem/intern.html', context)

