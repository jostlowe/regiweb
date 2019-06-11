from django.urls import path
from . import views

app_name = 'festkassen'
urlpatterns = [
    path('', views.forside, name='forside'),
    path('innskudd/', views.innskudd, name='innskudd'),
    path('admin/', views.admin, name='admin'),
    path('admin/innskudd', views.admin_innskudd, name='admin_innskudd'),
    path('admin/godkjenn_innskudd/<int:innskudd_pk>', views.admin_godkjenn_innskudd, name='admin_godkjenn_innskudd'),
    path('admin/krysselister', views.admin_interne_krysselister, name='admin_interne_krysselister'),
    path('admin/krysselister/<int:krysseliste_pk>', views.admin_rediger_krysseliste, name='admin_rediger_krysseliste'),
]

