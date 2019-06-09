#Django ORM models for database
from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
=======
class Product(models.Model):
    ProductName = models.CharField(max_length=100)
    Description = models.TextField()
    DateCreated = models.DateTimeField()

#class employee(models.Model):

class UserItems(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)    #Als User is verwijderd, verwijder deze rij ook
    item = models.ForeignKey(Product, on_delete=models.CASCADE)



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


>>>>>>> master
class EmpWithItems(models.Model):
    DateStart = models.TextField()
    DateEnd = models.TextField()
    rating = models.IntegerField()
<<<<<<< HEAD
    id = models.IntegerField(primary_key=True)

class Inventory(models.Model):
    ProductName = models.CharField(max_length=100)
    ProductImage = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)


=======
    Employees = models.ForeignKey(Employees, on_delete=models.CASCADE, default=0, related_name='employees')
    Inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default=0, related_name='inventory')
    id = models.IntegerField(primary_key=True)
>>>>>>> master
