from django.shortcuts import render
from django.views.generic import TemplateView

from product_app.models import Order, OrderItem


# Create your views here.


class HomeView(TemplateView):
    template_name = "home_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            order = Order.objects.filter(user=user, status="notRegistered").first()
            count = order.items.count() if order else 0
            context.update({
                'user': user,
                'order': order,
                'count': count
            })



        return context
