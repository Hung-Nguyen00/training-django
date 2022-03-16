from django.urls import path
from cart.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
urlpatterns = [
    path("product/", views.OrderProductView.as_view(), name="add-product-to-cart"),
    path("product/<product_id>/", views.UpdateOrderProductView.as_view(), name="edit-product-in-cart"),
    path("products/", views.OrderListView.as_view(), name="list-products-in-cart"),
]