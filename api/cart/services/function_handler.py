from product.models import Product
from cart.models import OrderProduct, Order


def create_or_update_order_product(order: Order, validated_data):
    product_id = validated_data.pop("product_id")
    amount = validated_data["amount"]
    is_buying = validated_data["is_buying"]
    
    product = Product.objects.get(id=product_id)
    total = product.selling_price * amount
    order_details, created = OrderProduct.objects.update_or_create(order=order, product=product, defaults={
        "total" : total, "amount" : amount, "price": product.selling_price, "is_buying": is_buying
    })
    return order_details
