from django.contrib import admin
from .models import Festkassekonto, Transaksjonstype, Transaksjon, Bar, Festkassekontotype
# Register your models here.

class FestkassekontoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kontotype',  'aktiv', 'pk', 'saldo')

    def saldo(self, obj):
        return obj.saldo()

class TransaksjonAdmin(admin.ModelAdmin):
    list_display = ('festkassekonto', 'transaksjonstype', 'sum', 'tidsstempel', 'bar')
    list_display_links = ('transaksjonstype', 'bar')


admin.site.register(Festkassekonto, FestkassekontoAdmin)
admin.site.register(Festkassekontotype)
admin.site.register(Transaksjonstype)
admin.site.register(Transaksjon, TransaksjonAdmin)
admin.site.register(Bar)
