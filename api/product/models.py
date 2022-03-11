import sys
from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel, SoftDeletableModel
from usermodel.models import User
from PIL import Image
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class Category(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField()
    parent_id = models.ForeignKey('self', related_name='sub_category', on_delete=models.SET_NULL, blank=True, null=True)
    is_show = models.BooleanField(default=True)
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
        
    def get_sub_category(self):
        return self.sub_category
        
    
class Color(TimeStampedModel, SoftDeletableModel):
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

        verbose_name = "Color"
        verbose_name_plural = "Colors"
        

class Product(TimeStampedModel, SoftDeletableModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=150, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    
    price = models.DecimalField(default=0, decimal_places=3, max_digits=10)
    amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["code"]),
            models.Index(fields=["slug", "name"]),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    
    
class Images(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.ImageField(upload_to='images')
    thumbnail_path = models.ImageField(upload_to='images')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["file_path"]),
        ]
        verbose_name = "Images"
        verbose_name_plural = "Images"
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.thumbnail_path = self.compressImage(self.thumbnail_path)
        super(Images, self).save(*args, **kwargs)
        
    def compressImage(self,uploadedImage):
        imageTemporary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemporaryResized = imageTemporary.resize((1020,573)) 
        imageTemporary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(
            outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None
        )
        return uploadedImage
        
        
class ProductColor(TimeStampedModel, SoftDeletableModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_color")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color_product")
    amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    
class ProductCategory(TimeStampedModel, SoftDeletableModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_category")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_product")
    