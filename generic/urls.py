from django.urls import path
from . import views

urlpatterns = [
    path('blank/', views.blank, name='Fantasy-blank')
]
