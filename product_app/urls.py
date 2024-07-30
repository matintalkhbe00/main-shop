from django.urls import path
from . import views

urlpatterns = [
    path('products_list', views.ProductListView.as_view(), name='product_list'),
]
