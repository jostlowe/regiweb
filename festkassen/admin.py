from django.contrib import admin
from .models import Festkassekonto, Transaksjon, Bar, Festkassekontotype, Vare
# Register your models here.


class FestkassekontoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kontotype',  'aktiv', 'pk', 'saldo')

    def saldo(self, obj):
        return obj.saldo()


class TransaksjonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'festkassekonto', 'vare',
                    'antall', 'stykkpris', 'sum', 'tidsstempel', 'godkjent',)
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


admin.site.register(Festkassekonto, FestkassekontoAdmin)
admin.site.register(Festkassekontotype)
admin.site.register(Transaksjon, TransaksjonAdmin)
admin.site.register(Bar)
admin.site.register(Vare, VareAdmin)
