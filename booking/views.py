from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Hotel
from .forms import HotelForm

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def about(request):
    return render(request, 'about.html')

class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'

class HotelCreateView(CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel-list')

class HotelUpdateView(UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel-list')

class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel-list')