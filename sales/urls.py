from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('record-sale/', views.record_sale, name='record_sale'),
    path('sales-summary/', views.sales_summary, name='sales_summary'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
]