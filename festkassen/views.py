from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Festkassekonto, Transaksjon, Vare
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def forside(request):
    context = {}
    return render(request, 'festkassen/forside.html', context)


@login_required
def innskudd(request):
    festkassekonto = Festkassekonto.objects.filter(regiweb_bruker=request.user).first()
    context = {
        'festkassekonto': festkassekonto
    }
    return render(request, 'festkassen/innskudd.html', context)


@login_required
def registrer_innskudd(request, ):
    vare = Vare.objects.get(navn='Innskudd')
    festkassekonto = get_object_or_404(Festkassekonto, regiweb_bruker=request.user)
    transaksjon = Transaksjon(
        vare=vare,
        stykkpris=int(request.POST['sum']),
        antall=1,
        festkassekonto=festkassekonto,
        godkjent=False
    )
    transaksjon.save()
    return HttpResponse("registret %s på %s" % (request.POST['sum'], request.user))

