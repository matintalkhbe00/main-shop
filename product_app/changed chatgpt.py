# class ProductAddOrderView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         user = request.user
#         product = get_object_or_404(Product, pk=pk)
#         quantity = int(request.POST.get('quantity', 1))
#
#         # دریافت یا ایجاد سفارش
#         order, created = Order.objects.get_or_create(status="notRegistered", user=user)
#
#         # بررسی وجود آیتم محصول در سفارش
#         order_item, item_created = OrderItem.objects.get_or_create(
#             order=order,
#             product=product,
#             defaults={'quantity': quantity, 'price': product.get_final_price()}
#         )
#
#         if not item_created:
#             # به‌روزرسانی تعداد و قیمت آیتم موجود
#             order_item.quantity += quantity
#             order_item.price = product.get_final_price()
#             order_item.save()
#
#         # به‌روزرسانی قیمت کل سفارش
#         order.update_total_price()
#
#         return redirect("product_app:order_detail")
#
#
# from django.db import transaction
#
# class ProductAddOrderView(LoginRequiredMixin, View):
#     @transaction.atomic
#     def post(self, request, pk):
#         user = request.user
#         product = get_object_or_404(Product, pk=pk)
#         quantity = int(request.POST.get('quantity', 1))
#
#         # دریافت یا ایجاد سفارش
#         order, created = Order.objects.get_or_create(status="notRegistered", user=user)
#
#         # بررسی وجود آیتم محصول در سفارش
#         order_item, item_created = OrderItem.objects.get_or_create(
#             order=order,
#             product=product,
#             defaults={'quantity': quantity, 'price': product.get_final_price()}
#         )
#
#         if not item_created:
#             # به‌روزرسانی تعداد و قیمت آیتم موجود
#             order_item.quantity += quantity
#             order_item.price = product.get_final_price()
#             order_item.save()
#
#         # به‌روزرسانی قیمت کل سفارش
#         order.update_total_price()
#
#         return redirect("product_app:order_detail")



# //////////////////////


from itertools import product

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from account_app.models import Address
from .forms import ProductReviewForm, ReplyForm, OrderItemUpdateForm, OrderItemDeleteForm, AddressForm
from .models import Product, ProductReview, Order, OrderItem, DiscountCode


def add_reply(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(ProductReview, id=review_id)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.product = review.product
            reply.author = request.user.fullname if request.user.fullname else request.user.phone
            reply.parent = review
            reply.save()
            return HttpResponseRedirect(reverse('product_app:product_detail', args=[review.product.id]))
    return HttpResponseRedirect(reverse('product_app:product_detail', args=[review.product.id]))


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_images = product.images.all()
        product_features = product.features.all()
        product_reviews = product.reviews.filter(parent__isnull=True).prefetch_related('replies')
        user_reviews = product.reviews.filter(author=request.user.phone)

        form = ProductReviewForm()

        context = {
            'product': product,
            'product_images': product_images,
            'product_features': product_features,
            'product_reviews': product_reviews,
            'form': form,
            'user_reviews': user_reviews,
        }

        return render(request, 'product_app/product_details.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user.phone
            parent_id = request.POST.get('parent_id')
            if parent_id:
                review.parent = ProductReview.objects.get(id=parent_id)
            review.save()
        return redirect('product_app:product_detail', pk=product.id)


class ProductListView(ListView):
    model = Product
    template_name = 'product_app/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_ratings = {product.pk: product.calculate_average_rating() for product in Product.objects.all()}
        context['products_with_ratings'] = products_with_ratings
        return context


# ////////////////////////////////////////////////////////////////


from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Product, Order, OrderItem, DiscountCode


class ProductAddOrderView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        discount_code = request.POST.get('discount_code', '').strip()

        # دریافت یا ایجاد سفارش
        # order, created = Order.objects.get_or_create(status="notRegistered", user=user)

        order = Order.objects.filter(user=user, status="notRegistered")
        if not order:
            order = Order.objects.create(user=user)

        # بررسی وجود آیتم محصول در سفارش
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity, 'price': product.get_final_price()}
        )

        if not item_created:
            # به‌روزرسانی تعداد و قیمت آیتم موجود
            order_item.quantity += quantity
            order_item.price = product.get_final_price()
            order_item.save()

        # به‌روزرسانی قیمت کل سفارش
        order.update_total_price()

        if discount_code:
            try:
                discount_code = DiscountCode.objects.get(name=discount_code)
                if discount_code.is_valid():
                    order.discount_code = discount_code
            except DiscountCode.DoesNotExist:
                pass

        order.save()

        return redirect("product_app:order_detail")


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'product_app/order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        addresses = Address.objects.filter(user=user)
        selected_address_id = self.request.session.get('selected_address_id')
        order = Order.objects.filter(user=user, status="notRegistered")
        context.update({
            'user': user,
            'addresses': addresses,
            'selected_address_id': selected_address_id,
            'form': AddressForm(),
            'orders': order,
        })

        return context


from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from .models import Order, DiscountCode


class ApplyDiscountView(View):
    def post(self, request):
        discount_code = request.POST.get('discount_code')

        if not discount_code:
            messages.error(request, 'لطفاً کد تخفیف را وارد کنید.')
            return redirect(reverse('product_app:order_detail'))

        order = Order.objects.filter(user=request.user, status='notRegistered').first()
        if not order:
            messages.error(request, 'سفارشی برای شما پیدا نشد.')
            return redirect(reverse('product_app:order_detail'))

        # جستجو کد تخفیف بدون استفاده از get_object_or_404
        try:
            discount = DiscountCode.objects.get(name=discount_code)
        except DiscountCode.DoesNotExist:
            messages.error(request, 'کد تخفیف معتبر نیست.')
            return redirect(reverse('product_app:order_detail'))

        if not discount.is_valid():
            messages.error(request, 'کد تخفیف معتبر نیست.')
            return redirect(reverse('product_app:order_detail'))

        # اعمال تخفیف به سفارش
        discount_amount = (order.original_price * discount.discount) / 100
        order.total_price = order.original_price - discount_amount
        order.discount_code = discount
        order.save()

        # کاهش تعداد کد تخفیف
        discount.quantity -= 1
        discount.save()

        messages.success(request, f'تخفیف {discount.discount}% به سفارش شما اعمال شد.')
        return redirect(reverse('product_app:order_detail'))


class RemoveDiscountView(View):
    def post(self, request):
        order = Order.objects.filter(status='notRegistered', user=request.user).first()

        if not order:
            messages.error(request, "سفارشی برای حذف تخفیف یافت نشد.")
            return redirect(reverse('product_app:order_detail'))

        if order.discount_code:
            # ذخیره کد تخفیف قبل از حذف
            discount = order.discount_code

            # حذف کد تخفیف از سفارش
            order.discount_code = None
            order.total_price = order.original_price
            order.save()

            # افزایش تعداد کد تخفیف
            discount.quantity += 1
            discount.save()

            messages.success(request, "کد تخفیف با موفقیت حذف شد.")
        else:
            messages.error(request, "هیچ کد تخفیفی برای حذف وجود ندارد.")

        return redirect(reverse('product_app:order_detail'))


class UpdateOrderItemView(View):
    def post(self, request, *args, **kwargs):
        form = OrderItemUpdateForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            order_item = get_object_or_404(OrderItem, id=item_id)
            quantity = form.cleaned_data['quantity']
            order_item.quantity = quantity
            order_item.save()
            return redirect('product_app:order_detail')  # Update the URL name accordingly


class DeleteOrderItemView(View):
    def post(self, request, *args, **kwargs):
        order_item_id = request.POST.get('order_item_id')

        if order_item_id:
            # تلاش برای دریافت OrderItem با شناسه داده شده
            order_item = get_object_or_404(OrderItem, id=order_item_id)
            order = order_item.order

            # حذف آیتم از سفارش
            order_item.delete()

            # بروزرسانی قیمت کل سفارش
            order.update_total_price()

            # هدایت به صفحه جزئیات سفارش
            return redirect('product_app:order_detail')
        else:
            # مدیریت خطا در صورت عدم ارسال شناسه آیتم
            return redirect('product_app:product_list')  # یا صفحه دیگری برای مدیریت خطا


class AddAddressView(LoginRequiredMixin, FormView):
    form_class = AddressForm
    success_url = reverse_lazy('product_app:order_detail')

    def form_valid(self, form):
        new_address = form.save(commit=False)
        new_address.user = self.request.user
        new_address.save()
        return super().form_valid(form)


def select_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    order = Order.objects.filter(user=request.user, status='notRegistered').first()

    if order:
        # تعیین آدرس برای سفارش
        order.address = address
        order.save()

    # ذخیره آدرس انتخاب شده در سشن
    request.session['selected_address_id'] = address.id

    return redirect('product_app:order_detail')



class ProductAddOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        order = Order.objects.filter(status = "notRegistered" , user = user)
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity',1))
        if order:
            order = Order.objects.get(status="notRegistered", user=user)
            flag = False
            for item in order.items.all():
                if item.product == product:
                    flag = True
                    OrderItem.objects.get(id=item.id, order=order).delete()
                    OrderItem.objects.create(order=order, product=product, quantity=quantity+item.quantity, price=product.get_final_price())
            if not flag:
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.get_final_price())
            pass
        else:
            order = Order.objects.create(user=user)
            OrderItem.objects.create(order=order, product=product, quantity=quantity , price=product.price)


        return redirect("product_app:order_detail")


class OrderDetailView(View):
    def get(self, request):
        order = Order.objects.all()
        return render(request, "product_app/order_details.html" , {"order":order})