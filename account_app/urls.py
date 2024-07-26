from django.urls import path

from . import views

app_name = 'account_app'

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('loginEmail', views.UserLoginEmail.as_view(), name='login_email'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('checkotp', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout', views.Logout, name='logout'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
]
