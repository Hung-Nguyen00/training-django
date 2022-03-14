from dataclasses import field
from rest_framework import serializers
from product.models import Product, Color, Images, Category, ProductColor
from rest_framework.validators import UniqueValidator
from product.services.product import update_color_product
from django.db import transaction

class ProductSimplifiedSerializer(serializers.ModelSerializer):
     class Meta:
        model = Product
        fields = ("id", "code", "name")
    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "code", "name")


class ProductColorSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    class Meta:
        model = ProductColor
        fields = ("color",)
                
class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Category.objects.all())])
    sub_category = serializers.SerializerMethodField()
    parent_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Category.objects.all())
    
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "sub_category", "parent_id")
        
    @classmethod    
    def get_sub_category(cls, obj):
        sub_category = []
        if obj.sub_category.exists():
            for sub in obj.sub_category.all():
                serializer = CategorySerializer(sub)
                sub_category.append(serializer.data)
        return sub_category  
        
        
class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail_path = serializers.ImageField(required=True)
    product_id = serializers.PrimaryKeyRelatedField(required=True, write_only=True, source="product", queryset=Product.objects.all())
    
    class Meta:
        model = Images
        fields = ("id", "file_path", "thumbnail_path", "product_id")        
        
        
class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    color_ids  = serializers.ListField(write_only=True, required=True, allow_empty=True)
    product_color = serializers.SerializerMethodField(read_only=True)
    slug    = serializers.SlugField(read_only=True)
    name    = serializers.CharField(max_length=100, required=True)
    code    = serializers.CharField(max_length=50, required=True, validators=[UniqueValidator(queryset=Product.objects.all())])
    buying_price   = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    selling_price  = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    amount  = serializers.IntegerField(min_value=1, default=1)
    is_active = serializers.BooleanField(default=True)
    is_top    = serializers.BooleanField(default=False)
    
    class Meta:
        model = Product
        fields = (
            "id", 
            "code",
            "slug",
            "name",
            "description",
            "content",
            "buying_price",
            "amount",
            "selling_price",
            "is_active",
            "is_top",
            "product_images",
            "color_ids",
            "product_color",
        )
    
    # @classmethod
    # def validate_color_ids(cls, ids):
    #     if len(ids) == 0:
    #         raise serializers.ValidationError("Please select at least 1 color.")
    #     if not Color.objects.filter(id__in=ids).exists():
    #         return serializers.ValidationError("The selected interest is invalid.")
    #     return ids
    
    @classmethod
    def get_product_color(cls, obj):
        return [{"id": it.color.id, "name": it.color.name} for it in obj.product_color.all()]
    
    @transaction.atomic
    def update(self, instance, validated_data):
        color_ids = validated_data.pop("color_ids")
        update_color_product(instance, color_ids)
        return super(ProductSerializer, self).update(instance, validated_data)
    
    @transaction.atomic
    def create(self, validated_data):
        color_ids = validated_data.pop("color_ids")
        product = Product.objects.create(**validated_data)
        update_color_product(product, color_ids)
        return product
        
    