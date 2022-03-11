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
        
        
class CategorySimplifiedSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = "__all__"
        
    @classmethod    
    def get_sub_category(cls, obj):
        sub_category = []
        if obj.sub_category.exists():
            for sub in obj.sub_category.all():
                serializer = CategorySimplifiedSerializer(sub)
                sub_category.append(serializer.data)
        return sub_category
        
                

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
    product_color = ColorSerializer(many=True, read_only=True)
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
                  "product_images",
                  "product_color"
        )
    