from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Service, Booking, Review
from .forms import SignUpForm, ServiceForm, BookingForm, ReviewForm, LoginForm, UserProfileForm
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied


def home(request):
    services = Service.objects.all()
    return render(request, 'booking/home.html', {'services': services})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booking:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'booking/signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_professional:
        services = Service.objects.filter(provider=request.user)
        bookings = Booking.objects.filter(service__provider=request.user)
    else:
        services = None
        bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'booking/dashboard.html', {'services': services, 'bookings': bookings})

@login_required
def service_detail(request, service_id):
    service = Service.objects.get(pk=service_id)
    reviews = Review.objects.filter(booking__service=service)
    return render(request, 'booking/service_detail.html', {'service': service, 'reviews': reviews})



def search_services(request):
    query = request.GET.get('q')
    services = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'booking/search_results.html', {'services': services, 'query': query})


def send_booking_confirmation_email(booking):
    subject = f'Booking Confirmation for {booking.service.name}'
    message = f'Your booking for {booking.service.name} on {booking.date} has been confirmed.'
    from_email = 'noreply@servicebooking.com'
    recipient_list = [booking.customer.email]
    send_mail(subject, message, from_email, recipient_list)

def update_service_rating(service):
    reviews = Review.objects.filter(booking__service=service)
    if reviews:
        service.average_rating = sum(review.rating for review in reviews) / len(reviews)
        service.save()


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('booking:dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'booking/user_profile.html', {'form': form})

@login_required
def review_service(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Check if the user is the customer who made the booking
    if booking.customer != request.user:
        raise PermissionDenied("You don't have permission to review this service.")
    
    # Check if the booking is completed and hasn't been reviewed yet
    if booking.status != 'COMPLETED' or hasattr(booking, 'review'):
        raise PermissionDenied("You can only review completed bookings that haven't been reviewed yet.")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            update_service_rating(booking.service)
            return redirect('booking:dashboard')
    else:
        form = ReviewForm()
    return render(request, 'booking/review_service.html', {'form': form, 'booking': booking})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.customer = request.user  # Set the customer here

            # Validate that the customer is not the service provider
            if booking.customer == booking.service.provider:
                form.add_error(None, "You cannot book your own service.")
            else:
                booking.save()
                send_booking_confirmation_email(booking)
                return redirect('booking:dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'booking/book_service.html', {'form': form, 'service': service})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('booking:login')


def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("booking:home")
        form = LoginForm()
        context = {"form": form, "title": "Login"}
        return render(request, "booking/login.html", context)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("booking:home")
                messages.success(request, f"Hi {user.username}, Welcome back!")

            else:
                return render(request, "booking/login.html", context)
                messages.error(request, "Please check your login information and try again")
