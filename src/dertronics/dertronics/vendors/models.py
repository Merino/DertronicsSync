from django.db import models

# Create your models here.

class SyncLog(models.Model):

    sku = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)

    created = models.DateField(auto_now=True, auto_now_add=True)
    modified = models.DateField(auto_now_add=True)
