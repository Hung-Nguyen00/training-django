from os import read
from rest_framework import serializers
from cart.models import Order, OrderProduct
from product.models import Product
from cart.enums import OrderStatus
from django.db.models import Sum
from cart.services.order import OrderService
from product.api.serializers import ProductSerializer
from django.db import transaction
from cart.services.function_handler import create_or_update_order_product


        
class OrderProductSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all().values_list("pk", flat=True), required=True, write_only=True)
    product = ProductSerializer(read_only=True)
    amount = serializers.IntegerField(required=True, min_value=1)
    is_buying =  serializers.BooleanField(required=True)
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=0)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=0)
    
    class Meta:
        model = OrderProduct
        fields = (
                "id", 
                "product_id",
                "amount",
                "price",
                "total",
                "created",
                "is_buying",
                "order",
                "product",
        )        
    
    def validate(self, data):
        product_id = data['product_id']
        product = Product.objects.get(pk=product_id)
        if data['amount'] > product.amount:
            raise serializers.ValidationError({"amount": "The quantity is not enough"})
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        order = OrderService(user).create_order_if_not_exists()
        order_product = create_or_update_order_product(order, validated_data)
        return OrderProductSerializer(order_product).data
    
    def update(self, instance, validated_data):
        amount = validated_data['amount']
        instance.amount = amount
        instance.total = amount * instance.price
        instance.save()
        return instance
    
    
    
class OrderSerializer(serializers.Serializer):
    order_details = OrderProductSerializer(many=True)
    total_money = serializers.SerializerMethodField(read_only=True)
    address = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=50)
    
    class Meta:
        model = Order
        fields = ("id", "code", "created_at", "status", "total_money", "address", "order_details")
        
    @classmethod
    def get_total_money(cls, obj):
        total_money = obj.order_details.aggregate(total_money=Sum("total"))["total_money"]
        if total_money:
            return total_money
        return 0
    