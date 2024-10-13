from django.contrib import admin
from .models import Cart, Cart_Item, Product, Category
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_Item)