from django.urls import path
from . import views

app_name = 'festkassen'
urlpatterns = [

    # offentlig
    path('', views.forside, name='forside'),
    path('innskudd/', views.innskudd, name='innskudd'),

    # Forside for admin
    path('admin/', views.admin, name='admin'),

    # Godkjenne innskudd
    path('admin/innskudd', views.admin_innskudd, name='admin_innskudd'),
    path('admin/godkjenn_innskudd/<int:innskudd_pk>', views.admin_godkjenn_innskudd, name='admin_godkjenn_innskudd'),

    # Interne krysselister
    path('admin/krysselister', views.admin_interne_krysselister, name='admin_interne_krysselister'),
    path('admin/krysselister/<int:krysseliste_pk>', views.admin_rediger_krysseliste, name='admin_rediger_krysseliste'),
    path('admin/krysselister/<int:krysseliste_pk>/slett/<int:kryss_pk>', views.admin_slett_kryss, name='admin_slett_kryss'),

    # BSFer
    path('admin/bsf', views.admin_bsfer, name='admin_bsfer'),
    path('admin/bsf/<int:bsf_pk>', views.admin_rediger_bsf, name='admin_rediger_bsf'),
    path('admin/bsf/<int:bsf_pk>/liste/<int:liste_pk>', views.admin_rediger_ekstern_liste, name='admin_rediger_ekstern_liste'),
]

