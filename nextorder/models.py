from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50)

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return '%s' % (self.branch_name)

class Customer(models.Model):
    phone_number = models.IntegerField(null=True)
    last_name = models.CharField(max_length = 100, blank=True)
    first_name = models.CharField(max_length = 100, blank=True)
    age = models.IntegerField(null=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length = 250, blank=True)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Product(models.Model):
    sku = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=100, blank=True)
    weight = models.FloatField()
    picture = models.ImageField(upload_to='media/')
    
    def __str__(self):
        return '%s' % (self.name)


class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True)
    order_branch = models.ForeignKey(Branch, blank=True, null=True)
    order_number = models.CharField(max_length=100, blank=True)
    order_date = models.DateField( blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
#    delivery_date = models.CharField(max_length=15, blank=True)
    payment_total = models.CharField(max_length=100, blank=True)
    payment_advance = models.CharField(max_length=100, blank=True)
    payment_balance = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s' % (self.order_number)


class Document(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')



