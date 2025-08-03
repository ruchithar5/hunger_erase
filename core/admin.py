from django.contrib import admin
from .models import FoodDonation, Profile  # ✅ Import Profile
from .models import Volunteer

@admin.register(FoodDonation)
class FoodDonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'food_description', 'quantity', 'created_at', 'picked_by_ngo', 'delivered']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']  # Shows username and role in admin panel

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('created_at',)
