from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import HotelViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]