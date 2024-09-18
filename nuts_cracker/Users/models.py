from django.db import models
from django.contrib.auth.models import User
import random


class OTP(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  code=models.CharField(max_length=6)
  used=models.BooleanField(default=False)

  def save(self, *args,**kwargs):
    if not self.code:
      self.code=str(random.randint(100000,999999))
    super().save(*args,**kwargs)
