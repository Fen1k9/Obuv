
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=50)


class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    login = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class Address(models.Model):
    postcode = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    house = models.CharField(max_length=20)


class Unit(models.Model):
    unit_name = models.CharField(max_length=50)


class Provider(models.Model):
    provider_name = models.CharField(max_length=200)


class Producer(models.Model):
    producer_id = models.AutoField(primary_key=True)
    producer_name = models.CharField(max_length=200)


class Category(models.Model):
    category_name = models.CharField(max_length=100)


class Product(models.Model):
    article = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    price = models.IntegerField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount_percent = models.IntegerField()
    stock_quantity = models.IntegerField()
    description = models.TextField()
    photo = models.CharField(max_length=255)


class Order(models.Model):
    order_date = models.DateField()
    delivery_date = models.DateField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_code = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()