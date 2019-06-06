#Django ORM models for database
from django.db import models
from django.contrib.auth.models import User

class EmpWithItems(models.Model):
    EmployeeId = models.IntegerField()
    DateStart = models.TextField()
    DateEnd = models.TextField()
    InventoryId = models.IntegerField()
    rating = models.IntegerField()
    id = models.IntegerField(primary_key=True)

class Inventory(models.Model):
    ProductName = models.CharField(max_length=100)
    ProductImage = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)


