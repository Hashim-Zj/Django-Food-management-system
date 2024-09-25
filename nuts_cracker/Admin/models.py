from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False)
    no_of_products = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True)
    quantity = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mrp = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the product instance first
        super().save(*args, **kwargs)

        # Update the product count in the category
        self.category.no_of_products = (
            self.category.products_set.count()
        )  # Count related products
        self.category.save()  # Save the updated category

    def delete(self, *args, **kwargs):
        # Update the product count in the category before deleting
        category = self.category
        super().delete(*args, **kwargs)  # Delete the product

        # Update the product count in the category
        category.no_of_products = (
            category.products_set.count()
        )  # Count related products
        category.save()  # Save the updated category
