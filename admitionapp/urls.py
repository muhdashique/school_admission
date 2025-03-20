from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
      path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('forms/', views.forms, name='forms'),
    path('request_otp/', views.request_otp, name='request_otp'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    
    # Also add aliases with hyphens to handle both versions
    path('request-otp/', views.request_otp, name='request-otp'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),

]
