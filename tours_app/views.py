from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from .models import Trip, Destination, Booking, SiteAppearance
from .forms import UserRegisterForm, BookingForm, TripSearchForm
from django.urls import reverse

def index(request):
    # If a staff/admin user visits the public index, send them to the admin dashboard.
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('admin:index'))

    featured_trips = Trip.objects.filter(is_active=True, is_full=False).order_by('-created_at')[:6]
    featured_destinations = Destination.objects.filter(is_featured=True)[:4]
    # Keep the public page available while a new deployment is waiting for
    # ``python manage.py migrate`` to create the appearance table.
    try:
        appearance, _ = SiteAppearance.objects.get_or_create(pk=1)
    except (OperationalError, ProgrammingError):
        appearance = SiteAppearance()
    context = {
        'featured_trips': featured_trips,
        'featured_destinations': featured_destinations,
        'appearance': appearance,
    }
    return render(request, 'tours_app/index.html', context)

def trips(request, page_title='Explore Safaris'):
    form = TripSearchForm(request.GET or None)
    trips_list = Trip.objects.filter(is_active=True, is_full=False)
    
    if form.is_valid():
        destination = form.cleaned_data.get('destination')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        trip_type = form.cleaned_data.get('trip_type')
        
        if destination:
            trips_list = trips_list.filter(
                Q(name__icontains=destination) |
                Q(destinations__name__icontains=destination) |
                Q(destinations__location__icontains=destination)
            ).distinct()
        if start_date:
            trips_list = trips_list.filter(start_date__gte=start_date)
        if end_date:
            trips_list = trips_list.filter(end_date__lte=end_date)
        if min_price:
            trips_list = trips_list.filter(price_per_person__gte=min_price)
        if max_price:
            trips_list = trips_list.filter(price_per_person__lte=max_price)
        if trip_type:
            trips_list = trips_list.filter(trip_type=trip_type)
    
    paginator = Paginator(trips_list, 9)
    page = request.GET.get('page')
    trips_page = paginator.get_page(page)
    
    context = {'trips': trips_page, 'form': form, 'page_title': page_title}
    return render(request, 'tours_app/trips.html', context)

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, is_active=True)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login first to book')
            return redirect('login')
        
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.trip = trip
            
            if booking.number_of_seats > trip.available_seats:
                messages.error(request, f'Sorry, only {trip.available_seats} seats left!')
                return redirect('trip_detail', trip_id=trip.id)
            
            try:
                booking.save()
            except ValidationError:
                form.add_error('number_of_seats', f'Sorry, only {trip.available_seats} seats left!')
            else:
                booking.send_admin_notification_email(request)
                messages.success(request, f'Booking successful! Booking ID: #{booking.id}')
                return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm(initial={
            'full_name': request.user.get_full_name() if request.user.is_authenticated else '',
            'email': request.user.email if request.user.is_authenticated else '',
        })
    
    context = {'trip': trip, 'form': form}
    return render(request, 'tours_app/trip_details.html', context)

def group_trips(request):
    request.GET = request.GET.copy()
    request.GET['trip_type'] = 'GROUP'
    return trips(request)

def contact(request):
    return render(request, 'tours_app/contact.html')

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'tours_app/booking_success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tours_app/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'CANCELLED':
        messages.warning(request, 'This booking is already cancelled')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        booking.cancel()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('my_bookings')
    
    return render(request, 'tours_app/cancel_booking.html', {'booking': booking})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to WILDFinder! Start booking your safari.')
            return redirect('index')
    else:
        form = UserRegisterForm()
    
    return render(request, 'tours_app/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            # Redirect staff users directly to admin dashboard
            if user.is_staff:
                return redirect(reverse('admin:index'))
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'tours_app/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('index')

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)[:5]
    context = {'user': request.user, 'bookings': bookings}
    return render(request, 'tours_app/profile.html', context)

from django.contrib.admin.views.decorators import staff_member_required
