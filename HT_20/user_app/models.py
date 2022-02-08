from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    category_fk = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, null=True)

    name = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Purchase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()




