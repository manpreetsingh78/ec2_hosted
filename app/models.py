from enum import unique
from django.db import models

# Create your models here.
class City(models.Model):
    id = models.AutoField(primary_key=True)
    city_name = models.CharField(null=True,max_length=255,unique=True)
    city_unique_id = models.IntegerField(null=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
class address(models.Model):
    id = models.AutoField(primary_key=True)
    city_id = models.ForeignKey(City,on_delete = models.CASCADE)
    address_field = models.TextField(unique=True)
    lat = models.DecimalField(max_digits=12, decimal_places=10)
    long = models.DecimalField(max_digits=12, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)