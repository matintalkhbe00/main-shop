from home_app.models import PhoneCompany, Footer
from product_app.models import Order, SubCategory


def user_cart_context(request):
    footer_info = Footer.objects.all().first()
    phone_company = PhoneCompany.objects.all()
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user, status="notRegistered").first()
        count = order.items.count() if order else 0
        return {
            'user': user,
            'order': order,
            'count': count,
            'footer_info': footer_info,
            'phone_company': phone_company
        }

    return {'footer_info': footer_info,
            'phone_company': phone_company}
