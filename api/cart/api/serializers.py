from os import read
from rest_framework import serializers
from cart.models import Order, OrderProduct
from product.models import Product
from cart.enums import OrderStatus
from cart.services.order import OrderService
from django.db import transaction
from cart.services.function_handler import create_or_update_order_product

class OrderSerializer(serializers.Serializer):
    
    class Meta:
        model = Order
        fields = ("id", "code", "created_at", "status", "total_money", "address")
        
        
class OrderProductSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all().values_list("id", flat=True), required=True, write_only=True)
    amount = serializers.IntegerField(required=True, min_value=1)
    is_buying =  serializers.BooleanField(required=True)
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=0)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=0)
    
    class Meta:
        model = OrderProduct
        fields = ("id", "product_id", "amount", "price", "total", "created", "is_buying")        
    
    def validate(self, data):
        product_id = data['product_id']
        product = Product.objects.get(pk=product_id)
        if data['amount'] > product.amount:
            raise serializers.ValidationError("The quantity is not enough")
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        order = OrderService(user).create_order_if_not_exists()
        product_id = validated_data.pop("product_id")
        order_product = create_or_update_order_product(product_id, validated_data['amount'], order)
        return OrderProductSerializer(order_product).data
        