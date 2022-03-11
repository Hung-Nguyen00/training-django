from rest_framework import serializers
from product.models import Product, Color, Images, Category
from usermodel.api.serializers import UserSerializer
from rest_framework.validators import UniqueValidator

class ProductSimplifiedSerializer(serializers.ModelSerializer):
     class Meta:
        model = Product
        fields = ("id", "code", "name")
    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "code", "name")
        

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField(required=True)
    
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "parent_id")        
        
        
class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        fields = ("id", "name", "file_path", "thumbnail_path")        
        
        
class ProductSerializer(serializers.ModelSerializer):
    product_color = ColorSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    code = serializers.CharField(max_length=50, required=True, validators=[UniqueValidator(queryset=Product.objects.all())])
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    amount = serializers.IntegerField(min_value=1, default=1)
    is_active = serializers.BooleanField(default=True)
    is_top = serializers.BooleanField(default=False)
    

    class Meta:
        model = Product
        fields = ("id", 
                  "code",
                  "slug",
                  "name",
                  "description",
                  "content",
                  "price",
                  "amount",
                  "is_active",
                  "is_top",
                  "images",
                  "product_color"
        )
    