from django.contrib import admin

# Register your models here.
from .models import Verv, Regifant, Vervperiode, Uke



class RegifantAdmin(admin.ModelAdmin):
    list_display = ('fornavn', 'etternavn', 'kallenavn', 'tatt_opp')
    list_display_links = ('fornavn', 'etternavn', 'kallenavn', 'tatt_opp')
    search_fields = ('fornavn', 'etternavn', 'tatt_opp')


class UkeAdmin(admin.ModelAdmin):
    list_display = ('ukenavn', 'aar')
    list_display_links = ('ukenavn', 'aar')
    search_fields = ('ukenavn', 'aar')


admin.site.register(Regifant, RegifantAdmin)
admin.site.register(Uke, UkeAdmin)
admin.site.register(Verv)
admin.site.register(Vervperiode)
