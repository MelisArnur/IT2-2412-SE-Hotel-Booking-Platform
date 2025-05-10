from rest_framework import serializers
from .models import Hotel, Booking

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'