from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail  # <-- import send_mail
from django.conf import settings  
from .forms import EmailLoginForm 
from .forms import VolunteerSignupForm     # <-- import settings to get EMAIL_HOST_USER

from .forms import FoodDonationForm, RegisterForm
from .models import FoodDonation

def faq(request):
    return render(request, 'core/faq.html')

def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            # Handle Remember Me
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # session expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            # Redirect based on role
            if hasattr(user, 'profile'):
                role = user.profile.role
                if role == 'donor':
                    return redirect('donate')
                elif role == 'ngo':
                    return redirect('view_donations')
                elif role == 'delivery':
                    return redirect('delivery_dashboard')  # change to your delivery view
            return redirect('home')  # fallback
    else:
        form = EmailLoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})

    

@login_required
def donate_view(request):
    if request.method == 'POST':
        form = FoodDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()

            # Send confirmation email
            subject = "Thank You for Your Food Donation!"
            message = f"Dear {request.user.username},\n\n" \
                      f"Thank you for donating food with Hunger Erase. Your generosity helps us fight hunger and reduce food waste.\n\n" \
                      f"Donation Details:\n" \
                      f"Description: {donation.food_description}\n" \
                      f"Quantity: {donation.quantity}\n\n" \
                      f"We appreciate your support!\n\n" \
                      f"Best regards,\n" \
                      f"Hunger Erase Team"

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, "Thank you for your donation! A confirmation email has been sent.")
            return redirect('home')
    else:
        form = FoodDonationForm()
    return render(request, 'core/donate.html', {'form': form})

@login_required
def view_donations(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'ngo':
        messages.warning(request, "Only NGO users can view donations.")
        return redirect('home')

    donations = FoodDonation.objects.all().order_by('-created_at')
    return render(request, 'core/view_donations.html', {'donations': donations})


@login_required
def mark_as_picked(request, donation_id):
    if not request.user.is_staff:
        messages.warning(request, "Only NGO staff can mark donations as picked.")
        return redirect('home')

    donation = get_object_or_404(FoodDonation, id=donation_id)
    donation.picked_by_ngo = True
    donation.save()
    messages.success(request, "Donation marked as picked.")
    return redirect('view_donations')

@login_required
def delivery_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'delivery':
        messages.warning(request, "Only Delivery Personnel can access this page.")
        return redirect('home')

    # Fetch all unpicked donations (or those assigned to delivery personnel)
    donations = FoodDonation.objects.filter(picked_by_ngo=True).order_by('-created_at')

    return render(request, 'core/delivery_dashboard.html', {'donations': donations})

def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            volunteer = form.save()  # Save the form and get volunteer instance

            # Send confirmation email
            send_mail(
                subject='Volunteer Registration Successful',
                message='🎉 Thank you for signing up to volunteer! 🙌 We appreciate your support. Someone from our team will contact you soon. Meanwhile, explore our site for more ways to help the community! 🌟❤️',
                from_email='ruchitha25reddy@gmail.com',   # Your email here
                recipient_list=[volunteer.email],          # Volunteer email from saved form
                fail_silently=False,
            )

            # Add a success message to show after redirect
            messages.success(request, "Thank you for signing up to volunteer! We will contact you soon.")
            
            return redirect('volunteer_signup')  # Or redirect to a thank you page
    else:
        form = VolunteerSignupForm()

    return render(request, 'core/volunteer_signup.html', {'form': form})