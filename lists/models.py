from django.db import models

# Create your models here.

class List(models.Model):
    def get_items(self):
        return Item.objects.filter(list=self)

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)