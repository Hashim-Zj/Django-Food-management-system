from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from Admin.models import Products
from django.core.validators import MinValueValidator, MaxValueValidator



class OTP(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="authenticate_by_otp"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used and (timezone.now() - self.created_at).seconds < 300

    def __str__(self):
        return f"OTP for {self.user.username}- Code: {self.code}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    pin_code = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    CART_STATUS_OPTIONS = (
        ("in-cart", "In Cart"),
        ("cancelled", "Cancelled"),
        ("order-placed", "Order Placed"),
    )
    status = models.CharField(max_length=100, default="in-cart", choices=CART_STATUS_OPTIONS)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} - {self.user.username}"
    
    
class Order(models.Model):
    # Linking directly to Product instead of Cart for flexibility
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    address = models.TextField(max_length=200)
    phone = models.CharField(
        max_length=15
    )  # Adjusted to CharField for more flexibility with phone numbers
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ORDER_STATUS_OPTIONS = (
        ("dispatched", "Dispatched"),
        ("cancelled", "Cancelled"),
        ("order-placed", "Order Placed"),
        ("delivered", "Delivered"),
    )
    status = models.CharField(
        max_length=100, default="order-placed", choices=ORDER_STATUS_OPTIONS
    )
    date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True)

    def __str__(self):
        return f"Order for {self.product.title} ({self.status})"


class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username} ({self.rating}/5)"
