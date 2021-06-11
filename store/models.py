from django.db import models
from category.models import Category
from ckeditor.fields import RichTextField

# Create your models here.

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.RESTRICT)
    product_name= models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/products',blank=True,null=True)
    facts_img = models.ImageField(upload_to='media/products/desc',blank=True,null=True)
    slug  = models.SlugField(max_length=100)
    description = RichTextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    is_avilable = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='product'
        verbose_name_plural='products'


    def __str__(self):
        return self.product_name


