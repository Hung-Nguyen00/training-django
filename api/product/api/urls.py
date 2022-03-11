from unicodedata import name
from django.urls import path
from product.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("colors", views.ColorView)
router.register("categories", views.CategoryView)

products_create_list = views.ProductView.as_view({
    "get": "list",
    "post": "create"
})

product_detail = views.ProductView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})

urlpatterns = [
    path('products/', products_create_list, name="products_list"),
    path('products/<pk>', product_detail, name="product_detail"),
] + router.urls