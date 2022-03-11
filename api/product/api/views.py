from re import X
from product.models import Product, Color, Category, Images
from product.api.serializers import ProductSerializer, ColorSerializer, CategorySerializer, ProductImageSerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from product.services.product import update_color_product

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    ordering_fields = '__all__'
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ColorView(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent_id__isnull=True)
    
    
    # def create(self, request):
    #     title = request.data.get('title')
    #     check_category_exist = Category.objects.filter(title=title).exists()
    #     if check_category_exist:
    #         return Response({"error": "This title is existed"}, status=status.HTTP_400_BAD_REQUEST)
    #     return super(CategoryView, self).create(request)
    
class ProductImagesView(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = Images.objects.all()
    
    def list(self, request,  *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        try:
            Product.objects.get(pk=product_id)
            queryset = self.queryset.filter(product_id=product_id)    
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"errors": "The product does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request,  *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        request.data['product_id'] = product_id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

