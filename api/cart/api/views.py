from cart.models import Order, OrderProduct
from rest_framework import generics, status, serializers
from cart.api.serializers import OrderSerializer, OrderProductSerializer
from cart.enums import OrderStatus
from rest_framework.response import Response
from product.exceptions import ProductDoesNotExistException, ThereAreNotAnyProductToOrderException
from cart.services.order import OrderService
from django.db import transaction
from cart.signals import dispatch_sending_email
from cart.permissions import IsOwnerOrder
from rest_framework import filters
import django_filters.rest_framework as django_filters


class OrderProductView(generics.ListCreateAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order = Order.objects.filter(
            user=self.request.user, status=OrderStatus.IS_SHOPPING).first()
        if not order:
            raise serializers.ValidationError("Your cart is empty")
        return OrderProduct.objects.filter(order=order)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [django_filters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code", "created"]
    filter_fields = ["total"]


class UpdateOrderProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderProductSerializer

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        order = Order.objects.filter(
            user=self.request.user, status=OrderStatus.IS_SHOPPING).first()
        try:
            order_detail = OrderProduct.objects.get(
                order=order, product_id=product_id)
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
    permission_classes = (IsOwnerOrder,)
    queryset = Order.objects.all().order_by("order_details__created")

    def get_object(self):
        return Order.objects.filter(user=self.request.user, status=OrderStatus.IS_SHOPPING).first()

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        data = request.data
        products = data.pop("products")
        product_ids = [product.get("product_id") for product in products]
        product_order = order.order_details.values_list(
            "product_id", flat=True)
        if not set(product_ids).issubset(product_order) or len(products) == 0:
            raise ThereAreNotAnyProductToOrderException()
        order_service = OrderService(request.user)
        code, checked = order_service.create_code()
        data["code"] = code
        data["status"] = OrderStatus.ORDERED.value
        serializer = OrderSerializer(instance=order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order_service.transfer_products_not_buy_to_new_order(
            order, list_products=products)
        dispatch_sending_email.send(sender=Order, order=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
