from django.contrib import admin
from .models import Cart, Cart_Item, Product, Category, Address, Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(Order)
admin.site.register(Address)