from django.contrib import admin
from .models import Product, ProductImage, ProductFeature, ProductReview, DiscountCode, Order, OrderItem

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
    list_filter = ('created_at', 'rating')

class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'quantity', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductFeature, ProductFeatureAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(Order, OrderAdmin)
