from product_app.models import Order

def user_cart_context(request):
    user = request.user
    order = Order.objects.filter(user=user, status="notRegistered").first()
    count = order.items.count() if order else 0
    return {
        'user': user,
        'order': order,
        'count': count
    }
