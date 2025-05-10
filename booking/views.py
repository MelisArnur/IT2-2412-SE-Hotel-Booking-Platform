from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from .models import Hotel, Booking
from .forms import HotelForm, RegisterForm, UpdateProfileForm, BookingForm
from rest_framework import viewsets 
from .serializers import HotelSerializer, BookingSerializer

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def about(request):
    return render(request, 'about.html')

class HotelListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'

    def test_func(self):
        return self.request.user.username == 'Arnur'

class HotelCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel-list')

    def test_func(self):
        return self.request.user.username == 'Arnur'

class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel-list')

    def test_func(self):
        return self.request.user.username == 'Arnur'

class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel-list')

    def test_func(self):
        return self.request.user.username == 'Arnur'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking-list')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)