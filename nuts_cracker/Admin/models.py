from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone
# Create your models here.

class Category(models.Model):
  category_name=models.CharField(max_length=50,null=False)
  no_of_products=models.PositiveIntegerField(default=0)
  status=models.BooleanField(default=False)

  def __str__(self):
    return self.category_name

class Products(models.Model):
  title=models.CharField(max_length=200,null=False)
  description=models.TextField(blank=True)
  quantity=models.CharField(max_length=50)
  stock=models.PositiveIntegerField()
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  mrp=models.PositiveIntegerField()
  price=models.PositiveIntegerField()
  image=models.ImageField(upload_to="products/",blank=True,null=True)
  
  def __str__(self):
    return self.title
