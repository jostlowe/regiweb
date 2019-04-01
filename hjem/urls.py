from django.urls import path
from . import views

app_name = 'hjem'
urlpatterns = [
    path('', views.index, name='index'),
    path('intern/', views.intern, name='intern'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('techspecs/', views.techspecs, name='techspecs'),
    path('om/', views.om, name='om')
]