from django.db import models
from store.models import Products
from accounts.models import Account


# Create your models here.

class Cart(models.Model):
    cartId = models.CharField(max_length=50, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cartId


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_totel(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.product_name
