from django.contrib import admin
from product.models import Product, Color, Category, Images, ProductCategory, ProductColor
from django.utils.safestring import mark_safe
from django.urls import reverse   
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "buying_price",
        "selling_price",
        "discount",
        "is_active"
    )
    search_fields = ("name", "is_active", "buying_price", "selling_price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "parent_id",
        "is_show",
    )
    search_fields = ("title", "is_show")


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "file_path", "product")
    search_fields = ("product",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "color", "amount")

    def product_name(self, obj):
        if obj.product:
            return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:product_product_change", args=(obj.product.pk,)),
            obj.product.name
        ))
        return ""


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "category")
    
    def product_name(self, obj):
        if obj.product:
            return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:product_product_change", args=(obj.product.pk,)),
            obj.product.name
        ))
        return ""
