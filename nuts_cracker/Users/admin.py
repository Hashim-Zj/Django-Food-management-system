from django.contrib import admin
from .models import OTP,Order,Payment

# Register your models here.
admin.site.register(OTP)
admin.site.register(Order)
admin.site.register(Payment)