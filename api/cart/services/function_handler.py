from product.models import Product
from cart.models import OrderProduct, Order



def create_or_update_order_product(product_id: int, amount: int, order: Order):
    product = Product.objects.get(id=product_id)
    total = product.buying_price * amount
    order_details, created = OrderProduct.objects.update_or_create(order=order, product=product, defaults={
        "total" : total, "amount" : amount, "price": product.buying_price
    })
    return order_details