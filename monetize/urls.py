from django.urls import path
from . import views

app_name = "monetize"

urlpatterns = [
    # Digital products
    path('products/', views.products_list, name='products_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:slug>/purchase/', views.purchase_product, name='purchase_product'),

    # Payments
    path('payment/<int:txn_id>/', views.product_payment, name='product_payment'),
    path('mpesa/pay/', views.start_stk_push, name='mpesa_pay'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]
