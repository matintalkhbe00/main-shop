from django.contrib import admin
from .models import Product, ProductImage, ProductFeature, ProductReview

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage', 'status', 'get_final_price', 'calculate_average_rating')
    list_filter = ('status', 'discount_percentage')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductFeatureInline, ProductReviewInline]

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('alt_text',)

class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('name', 'value')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'comment', 'created_at')
    search_fields = ('author', 'comment')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductFeature, ProductFeatureAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
