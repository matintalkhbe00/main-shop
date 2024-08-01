from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import ProductReviewForm, ReplyForm
from .models import Product, ProductReview

def add_reply(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(ProductReview, id=review_id)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.product = review.product
            if request.user.fullname:
                reply.author = request.user.fullname
            else:
                reply.author = request.user.phone
            reply.parent = review
            reply.save()
            # استفاده از reverse برای هدایت به صفحه محصول
            return HttpResponseRedirect(reverse('product_detail', args=[review.product.id]))
    # هدایت به صفحه محصول در صورت عدم POST یا فرم نامعتبر
    return HttpResponseRedirect(reverse('product_detail', args=[review.product.id]))

class ProductDetailView(View):
    def get(self, request, pk):
        # دریافت محصول بر اساس ID
        product = get_object_or_404(Product, pk=pk)

        # دریافت تصاویر محصول
        product_images = product.images.all()

        # دریافت ویژگی‌های محصول
        product_features = product.features.all()

        # دریافت نظرات محصول و نظرات پاسخ‌دار
        product_reviews = product.reviews.filter(parent__isnull=True).prefetch_related('replies')

        # دریافت نظرات کاربر جاری
        user_reviews = product.reviews.filter(author=request.user.phone)  # تصحیح فیلد نام کاربری

        # ایجاد فرم برای ارسال نظر
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
            review.author = request.user.phone  # تصحیح فیلد نام کاربری
            parent_id = request.POST.get('parent_id')
            if parent_id:
                review.parent = ProductReview.objects.get(id=parent_id)
            review.save()
        return redirect('product_detail', pk=product.id)

class ProductListView(ListView):
    model = Product
    template_name = 'product_app/product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # تعداد محصول در هر صفحه

    def get_context_data(self, **kwargs):
        # دریافت داده‌های پیش‌فرض
        context = super().get_context_data(**kwargs)

        # ایجاد دیکشنری برای نگهداری نمرات محصولات
        products_with_ratings = {product.pk: product.calculate_average_rating() for product in Product.objects.all()}

        # اضافه کردن محصولات با تعداد ستاره‌های رنگی به context
        context['products_with_ratings'] = products_with_ratings
        return context
