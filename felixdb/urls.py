from django.urls import path
from . import views

app_name = 'felixdb'
urlpatterns = [
    path('', views.index, name='index'),
    path('regifant/<int:regifant_id>/', views.regifant, name='regifant'),
    path('verv/', views.verv, name="verv"),
    path('verv/<int:verv_id>/', views.vervdetalj, name='vervdetalj'),
    path('ukeverv/', views.ukeverv, name="ukeverv"),
    path('ukeverv/<int:ukeverv_id>', views.ukevervdetalj, name="ukevervdetalj"),
    path('aarsoversikt/<int:aar>/', views.aarsoversikt, name='aarsoversikt'),
    path('uker/', views.uker, name='uker'),
    path('uker/<int:ukeaar>', views.ukedetalj, name='ukedetalj'),
]