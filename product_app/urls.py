# from django.urls import path
from . import views
#
# urlpatterns = [
#     path('products_list', views.ProductListView.as_view(), name='product_list'),
#     path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
#     path('reply/<int:review_id>/', views.add_reply, name='add_reply'),
# #     ////////////////////////////////////
#     path('order/add' , views.OrderCreationView.as_view(), name='order_create'),
#
# ]

from django.urls import path
from . import views

app_name = 'product_app'

urlpatterns = [
    path('reply/<int:review_id>/', views.add_reply, name='add_reply'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products', views.ProductListView.as_view(), name='product_list'),

    # ////////////////////////////////////////////////////////////////////////
    path('addproduct/<int:pk>', views.ProductAddOrderView.as_view(), name='product_add'),
    path('orderdetail' , views.OrderDetailView.as_view(), name='order_detail'),
    path('orderconfirm' , views.ConfirmOrderView.as_view(), name='order_confirm'),
    path('apply_discount/', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('remove_discount/', views.RemoveDiscountView.as_view(), name='remove_discount'),
    path('update_order_item/', views.UpdateOrderItemView.as_view(), name='update_order_item'),
    path('delete_order_item/', views.DeleteOrderItemView.as_view(), name='delete_order_item'),

    path('select_address/<int:address_id>/', views.select_address, name='select_address'),
    path('add_address/', views.AddAddressView.as_view(), name='add_address'),
]
