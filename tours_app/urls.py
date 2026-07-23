from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trips/', views.trips, name='trips'),
    path('trips/group/', views.group_trips, name='group_trips'),
    path('contact/', views.contact, name='contact'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
