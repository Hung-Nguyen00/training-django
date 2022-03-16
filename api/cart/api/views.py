from cart.models import Order, OrderProduct
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from cart.api.serializers import OrderSerializer, OrderProductSerializer
from cart.services.order import OrderService
from cart.enums import OrderStatus


class OrderProductView(generics.ListCreateAPIView):
    serializer_class = OrderProductSerializer
    
    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHIPPING).first()
        if not order:
            raise serializers.ValidationError("Your cart is empty")
        return OrderProduct.objects.filter(order=order)


            
    