from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    is_professional = models.BooleanField(default=False)

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    average_rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def clean(self):
        if not self.provider.is_professional:
            raise ValidationError("Only professional users can create services.")


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def clean(self):
        if hasattr(self, 'customer') and self.customer == self.service.provider:
            raise ValidationError("Users cannot book their own services.")

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.booking.status != 'COMPLETED':
            raise ValidationError("Only completed bookings can be reviewed.")
        if self.booking.customer != self.booking.service.provider:
            raise ValidationError("Only the customer who booked the service can leave a review.")
