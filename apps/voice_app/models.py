from django.db import models

# Create your models here.
class ItemList(models.Model):
    item = models.TextField()