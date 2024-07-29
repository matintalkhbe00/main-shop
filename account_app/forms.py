from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'ایمیل یا شماره تلفن خود را وارد کنید',
            'class': 'block w-full p-2 border border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white placeholder-gray-400',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور خود را وارد کنید',
            'class': 'block w-full p-2 border border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white placeholder-gray-400',
        })
    )


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تایید رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone", "profile_picture"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"
