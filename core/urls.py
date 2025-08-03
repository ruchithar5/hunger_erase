from django.urls import path ,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('donate/', views.donate_view, name='donate'),
    path('donations/', views.view_donations, name='view_donations'),
    path('mark-picked/<int:donation_id>/', views.mark_as_picked, name='mark_as_picked'),
    path('delivery-dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('faq/', views.faq, name='faq'),
    path('volunteer-signup/', views.volunteer_signup, name='volunteer_signup'),
    
]

