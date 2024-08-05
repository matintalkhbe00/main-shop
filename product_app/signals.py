# product_app/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, OrderItem, Order
from product_app.middleware import get_current_request

# سیگنال برای زمانی که یک محصول ذخیره می‌شود
@receiver(post_save, sender=Product)
def update_order_items_on_product_save(sender, instance, **kwargs):
    request = get_current_request()
    print('update_order_items_on_product_save')
    if request and request.user.is_authenticated:
        user = request.user
        if instance.status == 'out_of_stock':
            print('out-of-stock')
            # اگر وضعیت محصول "ناموجود" باشد، باید آن را از تمام لیست‌های خرید حذف کنیم
            affected_order_items = OrderItem.objects.filter(product=instance, order__user=user)
            affected_order_items.delete()

            # # به‌روزرسانی قیمت کل سفارشات بعد از حذف محصول
            # affected_orders = Order.objects.filter(items__in=affected_order_items, user=user).distinct()
            # for order in affected_orders:
            #     order.update_total_price()
            #
            order = Order.objects.filter(user = user , status='notRegistered').first()
            order.update_total_price()
            order.save()

# سیگنال برای زمانی که یک محصول حذف می‌شود
@receiver(post_delete, sender=Product)
def update_order_items_on_product_delete(sender, instance, **kwargs):
    request = get_current_request()
    if request and request.user.is_authenticated:
        user = request.user
        # وقتی محصول حذف می‌شود، آن را از تمام لیست‌های خرید حذف می‌کنیم
        affected_order_items = OrderItem.objects.filter(product=instance, order__user=user)
        affected_order_items.delete()

        # به‌روزرسانی قیمت کل سفارشات بعد از حذف محصول
        affected_orders = Order.objects.filter(items__product=instance, user=user).distinct()
        for order in affected_orders:
            order.update_total_price()




#
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Product, OrderItem, Order
#
# @receiver(post_save, sender=OrderItem)
# def update_order_total_price(sender, instance, **kwargs):
#     order = instance.order
#     order.update_total_price()
#
# @receiver(post_delete, sender=OrderItem)
# def update_order_total_price_on_delete(sender, instance, **kwargs):
#     order = instance.order
#     order.update_total_price()
