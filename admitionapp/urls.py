from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
    path('', views.index, name='index'),  # Ensure `home` exists in views.py
]
