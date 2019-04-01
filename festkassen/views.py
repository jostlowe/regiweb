from django.shortcuts import render

# Create your views here.

def forside(request):
    context = {}
    return render(request, 'festkassen/forside.html', context)
