from django.db import models
from django.contrib.auth.models import User

class FoodDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    food_description = models.TextField()
    quantity = models.CharField(max_length=100)
    pickup_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='food_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picked_by_ngo = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)  # <-- Add this field with default

    def __str__(self):
        return f"{self.donor.username} - {self.food_description[:30]}"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
        ('delivery', 'Delivery Personnel'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    availability = models.TextField(help_text="Describe your availability or preferred times.")
    areas_of_interest = models.CharField(
        max_length=100,
        help_text="E.g. food pickup, distribution, packing, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"