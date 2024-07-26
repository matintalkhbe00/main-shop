from random import randint

from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import LoginForm, LoginFormEmail, RegisterForm, Otp, CheckOtpForm, User ,Profile , AddressCreationsForm
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from uuid import uuid4
from .sms import verification


# Create your views here.

# def login(request):
#     return render(request , template_name="account_app/login.html")

class ProfileView(View):
    def get(self, request):
        form = Profile()
        return render(request,"account_app/profile.html", {'form': form})


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account_app/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect("/")
            else:
                form.add_error('phone', 'Username or password is incorrect')
        else:
            form.add_error('phone', 'Username or password is incorrect')
        return render(request, "account_app/login.html", {'form': form})



class UserLoginEmail(View):
    def get(self, request):
        form = LoginFormEmail()
        return render(request, "account_app/loginEmail.html", {'form': form})

    def post(self, request):
        form = LoginFormEmail(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=(User.objects.get(email=cd['email']).phone), password=cd['password'])
            print(user.email)
            print(User.objects.get(email=cd['email']).is_admin)
            if user is not None:
                login(request, user)
                print(user.is_authenticated)
                return redirect("/")
            else:
                form.add_error('email', 'Username or password is incorrect')
        else:
            form.add_error('email', 'Username or password is incorrect')
        return render(request, "account_app/loginEmail.html", {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account_app/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            randcode = randint(1000,9999)
            print(randcode)
            cd = form.cleaned_data
            # send sms
            # verification(str(cd['phone']), str(randcode))
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'],code=randcode, token=token)

            return redirect(reverse('account_app:check_otp')+f'?token={token}')

        else:
            form.add_error("phone", "invalid data")

        return render(request, "account_app/register.html", {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account_app/check_otp.html" , {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user , is_create= User.objects.get_or_create(phone=otp.phone, password=otp.phone)
                login(request, user)
                Otp.objects.get(token=token).delete()
                return redirect("/")
        else:
            form.add_error("phone", "invalid data")
        return render(request, "account_app/check_otp.html" , {'form': form})


def Logout(request):
    logout(request)
    return redirect(reverse('account_app:login'))

class AddAddressView(View):

    def get(self, request):
        form = AddressCreationsForm()
        return render(request, "account_app/add_address.html", {'form': form})
    def post(self,request):
        form = AddressCreationsForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)

        return render(request, "account_app/add_address.html", {'form': form})

