from django.urls import path
from cart.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
urlpatterns = [
    path("products/", views.OrderProductView.as_view(), name="add-product-to-cart")
]