#Django ORM models for database
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    ProductName = models.CharField(max_length=100)
    Description = models.TextField()
    DateCreated = models.DateTimeField()

#class employee(models.Model):

class UserItems(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)    #Als User is verwijderd, verwijder deze rij ook
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

class EmpWithItems(models.Model):
    EmployeeId = models.IntegerField()
    DateStart = models.TextField()
    DateEnd = models.TextField()
    InventoryId = models.IntegerField()
    rating = models.IntegerField()
    id = models.IntegerField(primary_key=True)

class Employees(models.Model):
    id = models.IntegerField(primary_key=True)
    Role = models.TextField()
    Active = models.BooleanField()
    DateJoined = models.TextField()
    WorkExperience = models.IntegerField()
    Location = models.TextField()

class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    ProductName = models.TextField()
    ProductCategory = models.TextField()
    Specifications = models.TextField()
    Description = models.TextField()
    SerialNumber = models.TextField()
    Price = models.FloatField()
    DateCreated = models.TextField()
    DateUpdated = models.TextField()
    Stock = models.IntegerField()
    Total = models.IntegerField()
    Terminated = models.IntegerField()
    IsLoanItem = models.IntegerField()
    Location = models.TextField()
