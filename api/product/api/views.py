from product.models import Product, Color, Category
from product.api.serializers import ProductSimplifiedSerializer, ProductSerializer, ColorSerializer, CategorySerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    ordering_fields = '__all__'
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ColorView(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    
    def create(self, request):
        title = request.data.get('title')
        print(title)
        check_category_exist = Category.objects.filter(title=title).exists()
        if check_category_exist:
            return Response({"error": "This title is existed"}, status=status.HTTP_400_BAD_REQUEST)
        return super(CategoryView, self).create(request)