from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import FoodDonation, Profile, Volunteer
import re




# -------------------- Food Donation Form --------------------
class FoodDonationForm(forms.ModelForm):
    class Meta:
        model = FoodDonation
        fields = ['food_description', 'quantity', 'pickup_address', 'contact_number', 'photo']


# -------------------- Register Form --------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


# -------------------- Custom Email Login Form --------------------
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No user found with this email.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError("Incorrect password.")

        cleaned_data['user'] = user
        return cleaned_data


# -------------------- Volunteer Signup Form --------------------
class VolunteerSignupForm(forms.ModelForm):
   

    class Meta:
        model = Volunteer
        fields = ['full_name', 'email', 'phone_number', 'availability', 'areas_of_interest']
        widgets = {
            'availability': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your availability'}),
            'areas_of_interest': forms.TextInput(attrs={'placeholder': 'e.g., pickup, distribution'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        pattern = r'^[6-9]\d{9}$'

        if not re.match(pattern, phone):
            raise forms.ValidationError("Enter a valid 10-digit Indian mobile number.")
        return phone
