from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
  category_name=models.CharField(max_length=50,null=False)
  no_of_prducts=models.PositiveIntegerField(default=0)

  def __str__(self):
    return self.category_name

class Products(models.Model):
  title=models.CharField(max_length=50,null=False)
  discription=models.CharField(max_length=300)
  quantity=models.PositiveIntegerField()
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  price=models.PositiveIntegerField()
  image=models.ImageField(upload_to="Media/Products")
  