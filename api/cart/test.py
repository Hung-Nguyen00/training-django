import json
from django.urls import reverse
from rest_framework import status
from core.tests import SetUpCredentialTestCase
from cart.models import OrderProduct, Order
from product.models import Product


class CartTest(SetUpCredentialTestCase):
    
    
    def setUp(self):
        super().setUp()
        data = {
            "product_id": self.product.id,
            "amount": 4,
            "is_buying": False
        }
        post_url = reverse("add-product-to-cart")
        res = self.client.post(post_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_products_to_cart_and_get_cart_successfully(self):
        get_url = reverse("add-product-to-cart")
        res = self.client.get(get_url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_cart_when_user_orders(self):
        amount = 2
        data = {
            "address": "TP.HCM",
            "products": [
                {
                    "product_id": self.product.id,
                    "amount": amount,
                    "is_buying": True
                }
            ]   
        }
        url = reverse("list-products-in-cart")
        res = self.client.patch(url, data, format="json")
      
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order_detail = res.data.get("order_details")[0]
        product_amount = Product.objects.get(pk=self.product.id).amount
        total_of_product_ordered = self.product.selling_price * amount
        
        self.assertEqual(int(order_detail["total"]), total_of_product_ordered)
        self.assertTrue(order_detail["is_buying"])
        self.assertEqual(product_amount, self.product.amount - amount)
        
        