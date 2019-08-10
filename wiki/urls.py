from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.WikisideListView.as_view(), name='index'),
    path('ny/', views.WikisideCreateView.as_view(), name='wikiside_create'),
    path('<slug:slug>/', views.WikisideDetailView.as_view(), name='wikiside'),
    path('<slug:slug>/ny/', views.RevisjonCreateView.as_view(), name='revisjon_create'),
]