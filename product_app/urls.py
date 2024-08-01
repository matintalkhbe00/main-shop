from django.urls import path
from . import views

urlpatterns = [
    path('products_list', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('reply/<int:review_id>/', views.add_reply, name='add_reply'),
]
