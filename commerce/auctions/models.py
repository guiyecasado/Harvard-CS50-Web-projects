from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    categoryName = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="post_author")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    bid = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="categoryname")

    def __str__(self):
        return self.title





