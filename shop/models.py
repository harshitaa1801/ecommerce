from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from cloudinary.models import CloudinaryField # Import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


def get_product_image_path(instance, filename):
    # instance is the Product object.
    # filename is the original name of the uploaded file.
    # This will create a path like: 'products/12/image.jpg'
    return f'products/{instance.category.name}/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=252, null=True, blank=True)
    image = models.ImageField(upload_to=get_product_image_path)
    description = models.TextField(null=True, blank=True)
    published_on = models.DateField(auto_now_add=True, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}'s Cart"


class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    

class Address(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s address"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Cart_Item)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=15, default='PENDING')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

