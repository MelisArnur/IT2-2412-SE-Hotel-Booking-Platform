from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/create/', views.HotelCreateView.as_view(), name='hotel-create'),
    path('hotels/<int:pk>/update/', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('hotels/<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel-delete'),
]