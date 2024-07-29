from django.urls import path

from . import views

app_name = 'account_app'

urlpatterns = [
    path('login' , views.LoginView.as_view(), name='login'),
    path('signup' , views.SignupView.as_view(), name='signup'),
    path('products' , views.ProductListView.as_view(), name='products'),
    path('profile' , views.ProfileView.as_view(), name='profile'),
]