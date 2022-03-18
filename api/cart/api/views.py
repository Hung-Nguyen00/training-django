from cart.models import Order, OrderProduct
from rest_framework import generics, status, serializers
from cart.api.serializers import OrderSerializer, OrderProductSerializer
from cart.enums import OrderStatus
from rest_framework.response import Response
from product.exceptions import ProductDoesNotExistException, ThereAreNotAnyProductToOrderException
from cart.services.order import OrderService
from django.db import transaction
from cart.services.send_mail import OrderEmailService


class OrderProductView(generics.ListCreateAPIView):
    serializer_class = OrderProductSerializer
    
    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHOPPING).first()
        if not order:
            raise serializers.ValidationError("Your cart is empty")
        return OrderProduct.objects.filter(order=order)

class UpdateOrderProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderProductSerializer
    
    def get_object(self):
        product_id = self.kwargs.get('product_id')
        order = Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHOPPING).first()
        try:
            order_detail = OrderProduct.objects.get(order=order, product_id=product_id)
        except OrderProduct.DoesNotExist:
            raise ProductDoesNotExistException()
        return order_detail
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("order_details__created")
    
    def get_object(self):
        return Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHOPPING).first()

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        if not order.order_details.exists():
            raise ThereAreNotAnyProductToOrderException()
        order_service = OrderService(request.user)
        code, checked = order_service.create_code()
        data = request.data
        data["code"] = code
        data["status"] = OrderStatus.ORDERED.value
        data.pop("products")
        serializer = OrderSerializer(instance=order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        order_service.transfer_products_not_buy_to_new_order(order)
        OrderEmailService.send_mail_to_admin_when_user_ordered(order_id=order.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
