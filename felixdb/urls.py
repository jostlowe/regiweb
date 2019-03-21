from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('regifant/<int:regifant_id>/', views.regifant, name='regifant'),
    path('aarsoversikt/<int:aar>/', views.aarsoversikt, name='aarsoversikt'),
    path('verv/', views.verv, name="verv"),
    path('verv/<int:verv_id>/', views.vervdetalj, name='vervdetalj')
]