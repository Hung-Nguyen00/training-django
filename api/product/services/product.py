from product.models import Product, Color, ProductColor

def update_color_product(product: Product, color_ids: list[Color]):
    if len(color_ids) == 0:
        ProductColor.objects.filter(product=product).delete()
        return product
    product_color = ProductColor.objects.filter(product=product, color_id__in=color_ids)
    product_color_ids = product_color.values_list("color_id", flat=True)
    new_color_ids = [color_id for color_id in color_ids if color_id not in product_color_ids]
    new_product_color = []
    for color_id in new_color_ids:
        new_product_color.append(ProductColor(color_id=color_id, product=product))
    ProductColor.objects.bulk_create(new_product_color)
    return product
    
    
    