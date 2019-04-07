from django.contrib import admin
from .models import Festkassekonto, Festkassekontotype
from .models import Transaksjon, Vare, Krysseliste, Krysselistetype, Bar
from .models import BSF, Eksternkrysseliste, EksternDranker, EksternTransaksjon, BSFRegning
# Register your models here.


class FestkassekontoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kontotype',  'aktiv', 'pk', 'saldo')

    def saldo(self, obj):
        return obj.saldo()


class TransaksjonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'festkassekonto', 'vare',
                    'antall', 'stykkpris', 'sum', 'tidsstempel',
                    'krysseliste', 'godkjent',)
    list_display_links = ('__str__', 'festkassekonto')
    search_fields = (
        'festkassekonto__regiweb_bruker__first_name',
        'festkassekonto__regiweb_bruker__last_name',
        'festkassekonto__regiweb_bruker__username',
    )

    def sum(self, obj):
        return obj.sum()


class VareAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'standardpris', 'er_additiv', 'beskrivelse', )


class KrysselisteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'opprettet_av')


class BSFAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dato')


class EksternkrysselisteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bsf')


class EksternDrankerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bartilhorighet')


class EksterntransaksjonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'person', 'vare',
                    'antall', 'stykkpris', 'sum', 'tidsstempel', 'eksternkrysseliste',)


class BSFRegningAdmin(admin.ModelAdmin):
    list_display =('festkassekonto', 'bsf', 'bar', 'sum')


admin.site.register(Festkassekonto, FestkassekontoAdmin)
admin.site.register(Festkassekontotype)
admin.site.register(Transaksjon, TransaksjonAdmin)
admin.site.register(Bar)
admin.site.register(BSF, BSFAdmin)
admin.site.register(EksternTransaksjon, EksterntransaksjonAdmin)
admin.site.register(EksternDranker, EksternDrankerAdmin)
admin.site.register(Eksternkrysseliste, EksternkrysselisteAdmin)
admin.site.register(Vare, VareAdmin)
admin.site.register(Krysseliste, KrysselisteAdmin)
admin.site.register(Krysselistetype)
admin.site.register(BSFRegning, BSFRegningAdmin)
