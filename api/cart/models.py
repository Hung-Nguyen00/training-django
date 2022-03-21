from email.policy import default
from random import choices
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from usermodel.models import User
from cart.enums import OrderStatus
from product.models import Product
from django.db.models import Sum, F


class Order(TimeStampedModel, SoftDeletableModel):
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        choices=OrderStatus.choices(), blank=True, null=True, max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True)

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        total = self.order_details.aggregate(total_money=Sum("total", filter=F("is_buying") == True))['total_money']
        self.total = total if total else 0
        super(Order, self).save(*args, **kwargs)


class OrderProduct(TimeStampedModel, SoftDeletableModel):
    order = models.ForeignKey(
        Order, related_name="order_details", on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        Product, related_name="product_order", on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.PositiveIntegerField(default=1, null=True, blank=True)
    price = models.DecimalField(
        default=0, null=True, decimal_places=0, max_digits=10)
    total = models.DecimalField(
        default=0, null=True, decimal_places=0, max_digits=10)
    is_buying = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.total)

    def save(self, *args, **kwargs):
        self.total = self.price * self.amount
        super(OrderProduct, self).save(*args, **kwargs)
