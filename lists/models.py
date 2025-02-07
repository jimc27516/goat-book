from django.db import models

# Create your models here.

# TODO: support multiple users with different lists
# TODO: support mulitple lists per user
#    TODO:  unique url for each list
#    TODO:  url for creating a new list via POST
#    TODO:  url for adding a new item to an existing list via POST
class Item(models.Model):
    text = models.TextField(default="")