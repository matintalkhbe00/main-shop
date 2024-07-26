from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django import forms



class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError("Users must have an phone address")

        user = self.model(
            phone = phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, d and password.
        """
        user = self.create_user(
            phone,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="ایمیل",
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    fullname = models.CharField(max_length=50,null=True,blank=True, verbose_name="نام کامل")
    phone = models.CharField(max_length=12, unique=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def __str__(self):
        return self.phone  # برگرداندن شماره تلفن به جای ایمیل

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginFormEmail(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(11)])

class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(4)])


class Otp(models.Model):
    token = models.CharField(max_length=1000 , unique=True)
    phone = models.CharField(max_length=11, unique=True)
    code = models.SmallIntegerField()
    expiration_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.phone



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='address')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True , null=True )
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.phone


class AddressCreationsForm(forms.ModelForm):
    user = forms.IntegerField(required=False)
    class Meta:
        model = Address
        fields = "__all__"
