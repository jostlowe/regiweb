from django.urls import path
from . import views

app_name = 'festkassen'
urlpatterns = [
    path('', views.forside, name='forside'),
    path('innskudd/', views.innskudd, name='innskudd'),
]

