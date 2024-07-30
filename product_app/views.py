from django.views.generic import ListView
from .models import Product


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
