from django.contrib import admin
from cart.models import Order, OrderProduct
from django.utils.safestring import mark_safe
from django.urls import reverse
from core.utils import mark_safe_url
from django.utils.html import format_html
from django.template.loader import render_to_string
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "products",
        "total",
        "status",
        "address",
        "created",
    )
    search_fields = ("user__email", "created", "status")

    def products(self, obj):
        name = "admin:product_product_change"
        products = ""
        order_details = obj.order_details.all()
        for detail in order_details:
            products = products + " " + mark_safe_url(detail.product.id, name, detail.product.code)
        products = products.strip().replace(" ", " | ")
        return format_html(products)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product_name",
        "price",
        "amount",
        "total",
        "is_buying",
        "created",
    )
    search_fields = ("is_buying", "created", "product__name")
    list_filter = ("product__name",)

    def product_name(self, obj):
        if obj.product:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:product_product_change",
                        args=(obj.product.pk,)),
                obj.product.name
            ))
        return ""
