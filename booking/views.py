from django.shortcuts import render
from .models import Hotel

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def about(request):
    return render(request, 'about.html')