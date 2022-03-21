from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse, path, include
from usermodel.models import User
from product.models import Product

# Create your tests here.

class SetUpCredentialTestCase(APITestCase):
    urlpatterns = [
        path("v1/", include("config.api")),
    ]

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="Aa@123321",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        self.product = Product.objects.create(
            code="ASSS221", name="test", buying_price=200000, amount=10, selling_price=3000000)

        self.client = APIClient()
        url = reverse("token_obtain_pair")

        res = self.client.post(
            url, 
            {"email": "test@gmail.com", "password": "Aa@123321"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in res.data)
        self.token = res.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        
        return super().setUp()
    
