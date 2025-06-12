from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from .models import Hotel, Booking, Review, Room
from .forms import HotelForm, RegisterForm, UpdateProfileForm, BookingForm
from rest_framework import viewsets
from .serializers import HotelSerializer, BookingSerializer
from datetime import datetime

def custom_logout(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})

def home(request):
    location = request.GET.get('location', '')
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')

    hotels = Hotel.objects.all()
    if location:
        hotels = hotels.filter(location__icontains=location)
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
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bookings': bookings})

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
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

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

@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date() if check_in else None
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date() if check_out else None
    except (ValueError, TypeError):
        check_in_date = None
        check_out_date = None

    available_rooms = []
    if check_in_date and check_out_date:
        for room in rooms:
            conflicting_bookings = room.bookings.filter(
                check_out__gt=check_in_date,
                check_in__lt=check_out_date
            )
            if not conflicting_bookings.exists():
                available_rooms.append(room)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to make a booking.")
            return redirect('login')

        room_id = request.POST.get('room_id')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('booking:book_hotel', hotel_id=hotel_id)

        if check_in_date >= check_out_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('booking:book_hotel', hotel_id=hotel_id)

        room = get_object_or_404(Room, id=room_id, hotel=hotel)
        conflicting_bookings = room.bookings.filter(
            check_out__gt=check_in_date,
            check_in__lt=check_out_date
        )
        if conflicting_bookings.exists():
            messages.error(request, "This room is already booked for the selected dates.")
            return redirect('booking:book_hotel', hotel_id=hotel_id)

        Booking.objects.create(
            user=request.user,
            hotel=hotel,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date
        )
        messages.success(request, "Booking successful!")
        return redirect('booking:booking-list')  # Редирект на список бронирований

    return render(request, 'book_hotel.html', {
        'hotel': hotel,
        'available_rooms': available_rooms,
        'check_in': check_in,
        'check_out': check_out,
    })

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

@login_required
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            hotel=hotel,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('hotel_detail', pk=pk)
    return render(request, 'hotel_detail.html', {'hotel': hotel})