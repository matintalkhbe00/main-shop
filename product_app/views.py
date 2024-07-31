from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product


class ProductDetailView(View):
    def get(self, request, pk):
        # دریافت محصول بر اساس ID
        product = get_object_or_404(Product, pk=pk)

        # دریافت تصاویر محصول
        product_images = product.images.all()

        # دریافت ویژگی‌های محصول
        product_features = product.features.all()

        # دریافت نظرات محصول
        product_reviews = product.reviews.all()

        context = {
            'product': product,
            'product_images': product_images,
            'product_features': product_features,
            'product_reviews': product_reviews,
        }

        return render(request, 'product_app/product_details.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'product_app/product_list.html'
    context_object_name = 'products'
    paginate_by = 1 # تعداد محصول در هر صفحه

    def get_context_data(self, **kwargs):
        # دریافت داده‌های پیش‌فرض
        context = super().get_context_data(**kwargs)

        # ایجاد دیکشنری برای نگهداری نمرات محصولات
        products_with_ratings = {product.pk: product.calculate_average_rating() for product in Product.objects.all()}

        # اضافه کردن محصولات با تعداد ستاره‌های رنگی به context
        context['products_with_ratings'] = products_with_ratings
        return context
