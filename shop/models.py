from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='shop/images')
    description = models.TextField()
    published_on = models.DateField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

