from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Trip

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'full_name', 'email', 'phone_number', 'country', 'city',
            'tourist_type', 'pickup_point', 'number_of_seats', 'special_requests',
            'needs_airport_pickup', 'flight_number', 'arrival_time'
        ]
        widgets = {
            'tourist_type': forms.Select(attrs={'class': 'select-field'}),
            'pickup_point': forms.Select(attrs={'class': 'select-field'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

class TripSearchForm(forms.Form):
    destination = forms.CharField(max_length=200, required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    trip_type = forms.ChoiceField(choices=[('', 'All')] + list(Trip.TRIP_TYPES), required=False)