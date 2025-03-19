from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Ensure 'home.html' exists in templates
