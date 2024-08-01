from django.db import models


class Product(models.Model):
    PRODUCT_STATUS_CHOICES = [
        ('in_stock', 'موجود'),
        ('out_of_stock', 'ناموجود'),
    ]

    name = models.CharField(max_length=255, verbose_name='نام محصول')
    description = models.TextField(verbose_name='توضیحات محصول')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True,
                                              verbose_name='درصد تخفیف')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='in_stock', verbose_name='وضعیت')

    def get_final_price(self):
        if self.discount_percentage and self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    def calculate_average_rating(self):
        reviews = self.reviews.all()
        sum_rating = 0.0
        count = 0

        for review in reviews:
            if review.rating is not None:
                sum_rating += review.rating
                count += 1

        if count > 0:
            return sum_rating / count
        else:
            return 0.0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, verbose_name='محصول')
    name = models.CharField(max_length=255, verbose_name='ویژگی')
    value = models.CharField(max_length=255, verbose_name='مقدار ویژگی')

    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی‌های محصول'


class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='محصول')
    author = models.CharField(max_length=255, verbose_name='نویسنده')
    rating = models.FloatField(verbose_name='امتیاز', null=True, blank=True)
    comment = models.TextField(verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE,
                               verbose_name='پاسخ به')

    def __str__(self):
        return f"نظر {self.author} بر روی {self.product.name}"

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'
        ordering = ['-created_at']
