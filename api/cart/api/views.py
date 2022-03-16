from cart.models import Order, OrderProduct
from rest_framework import generics, status, serializers
from cart.api.serializers import OrderSerializer, OrderProductSerializer
from cart.enums import OrderStatus
from rest_framework.response import Response

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
            raise serializers.ValidationError({"error": "This product does not exist"})
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
        
        
class OrderListView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("order_details__created")
    
    def get_object(self):
        return Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHOPPING).first()
        