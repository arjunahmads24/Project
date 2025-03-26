from django.db import models
from django.utils import timezone

class Email(models.Model):
    email = models.EmailField()
    datetime_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
