from django.contrib import admin
from .models import Product, SaleTransaction, SaleItem

admin.site.register(Product)
admin.site.register(SaleTransaction)
admin.site.register(SaleItem)

# Register your models here.
