from django.contrib import admin
from .models import Festkassekonto, Festkassekontotype
from .models import Vare, Krysseliste, Krysselistetype, Bar
from .models import BSF, Eksternkrysseliste, EksternDranker, EksternTransaksjon
from .models import Kryss, BSFregning, Innskudd
# Register your models here.


class FestkassekontoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kontotype',  'aktiv', 'pk')


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


class InnskuddAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'festkassekonto', 'belop', 'godkjent', 'er_utlegg')


class BSFregningAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'festkassekonto', 'belop', 'bar', 'bsf')


class KryssAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'festkassekonto', 'vare', 'antall', 'stykkpris', 'sum', 'krysseliste')

    @staticmethod
    def sum(obj):
        return obj.sum()


admin.site.register(Festkassekonto, FestkassekontoAdmin)
admin.site.register(Festkassekontotype)
admin.site.register(Bar)
admin.site.register(BSF, BSFAdmin)
admin.site.register(EksternTransaksjon, EksterntransaksjonAdmin)
admin.site.register(EksternDranker, EksternDrankerAdmin)
admin.site.register(Eksternkrysseliste, EksternkrysselisteAdmin)
admin.site.register(Vare, VareAdmin)
admin.site.register(Krysseliste, KrysselisteAdmin)
admin.site.register(Krysselistetype)
admin.site.register(BSFregning)
admin.site.register(Innskudd, InnskuddAdmin)
admin.site.register(Kryss, KryssAdmin)
