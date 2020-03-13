from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Fantasy-home'),
    path('about/', views.about, name='Fantasy-about'),
    path('fixtures/', views.fixtures, name='Fantasy-fixtures'),
    path('allplayers/', views.allPlayers, name='Fantasy-allplayers'),
    path('squadselection/', views.squadSelectionView, name='Fantasy-squadSelection'),
    path('register/',views.register, name='Fantasy-register'),
]
