from django.urls import path
from product.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("colors", views.ColorView)
router.register("categories", views.CategoryView)

images_product_create_list = views.ProductImagesView.as_view({"get": "list", "post": "create"})
products_create_list = views.ProductView.as_view({"get": "list", "post": "create"})
product_detail = views.ProductView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})

urlpatterns = [
    path('products/', products_create_list, name="products_list"),
    path('products/<pk>/', product_detail, name="product_detail"),
    path('products/<product_id>/images/', images_product_create_list, name="product_images"),
] + router.urls