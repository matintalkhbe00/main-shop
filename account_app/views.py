from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from product_app.forms import AddressForm
from product_app.models import Order
from .forms import CustomLoginForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# Create your views here.

class LoginView(FormView):
    template_name = 'account_app/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')  # به صفحه‌ای که پس از ورود موفقیت‌آمیز کاربر هدایت می‌شود، تغییر دهید

    def dispatch(self, request, *args, **kwargs):
        # اگر کاربر قبلاً وارد سیستم شده باشد، او را به صفحه اصلی هدایت کن و پیام مناسب را اضافه کن
        if request.user.is_authenticated:
            messages.info(request, 'شما قبلاً وارد سیستم شده‌اید.')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'نام کاربری یا رمز عبور نادرست است.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
class SignupView(TemplateView):
    template_name = "account_app/signup.html"

class ProductListView(TemplateView):
    template_name = "account_app/product.html"

from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "account_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        order = Order.objects.all().order_by('-id')
        notification_type = self.request.GET.get('notification')
        if notification_type == 'confirmOrder':
            show_notification = True
            notification_message = 'پرداخت با موفقیت انجام شد!'
        else:
            show_notification = False
            notification_message = ''
        context.update({
            'user': user,
            'orders': order,
            'show_notification': show_notification,
            'notification_message': notification_message
        })

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # اگر کاربر وارد نشده است، او را به صفحه ثبت‌نام هدایت کن
            return redirect('account_app:login')  # فرض کنید نام URL صفحه ثبت‌نام 'signup' است
        return super().get(request, *args, **kwargs)




@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('product_app:order_details')  # یا هر URL دیگری که مناسب باشد
    else:
        form = AddressForm()

    return render(request, 'account_app/add_address.html', {'form': form})


