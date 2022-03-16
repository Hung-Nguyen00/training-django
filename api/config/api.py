from django.urls import include, path

urlpatterns = [
    path("", include("user_auth.api.urls")),
    path("", include("product.api.urls")),
    path("cart/", include("cart.api.urls")),
]
 