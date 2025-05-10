from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, Booking

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hotel', 'check_in', 'check_out']