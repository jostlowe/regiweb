from .models import Wikiside, Revisjon
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import reverse


# Lister opp alle wikisidene laget
class WikisideListView(ListView):
    template_name = 'wiki/index.html'
    queryset = Wikiside.objects.all().order_by('tittel')


# Viser ønsket wikiside
class WikisideDetailView(DetailView):
    template_name = 'wiki/wikiside.html'
    model = Wikiside

    def get_success_url(self):
        return reverse('wikiside', kwargs={'slug': self.object.slug})


# Oppretter wikiside
class WikisideCreateView(CreateView):
    template_name = 'wiki/wikiside_create.html'
    model = Wikiside
    fields = ['tittel']

    def get_success_url(self):
        return reverse('wiki:revisjon_create', kwargs={'slug': self.object.slug})


# Oppretter ny revisjon for wikisiden

class RevisjonCreateView(CreateView):
    template_name = 'wiki/revisjon_create.html'
    model = Revisjon
    fields = ['innhold', 'kommentar']

    def get_initial(self):
        innhold = Revisjon.objects.latest('sist_endret').innhold
        return {
            'innhold': innhold,
        }

    def form_valid(self, form):
        form.instance.forfatter = self.request.user
        form.instance.wikiside = Wikiside.objects.latest('dato_opprettet')
        return super(RevisjonCreateView, self).form_valid(form)

    def get_success_url(self):
        wikiside = self.object.wikiside
        return reverse('wiki:wikiside', kwargs={'slug': wikiside.slug})
