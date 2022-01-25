from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from .forms import CreateUserForm
from sqlalchemy import null
# Create your models here.


class Customer(models.Model):
    # one-to-one --> a user can only have one customer and one customer can have one user
    # upon customer deletion, we must delete everythin related to it
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=False)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):  
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

# Order will be the summary of items order and a transaction_id. order-->cart and order_items-->items in cart
class Order(models.Model):
    # many-to-one --> one customer can have many orders and upon order deletion we should set it to null
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):  
        return str(self.id)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) 
        return round(total,2)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) 
        return total


class OrderItem(models.Model):
    # many-to-one --> one order can have many order_items
    # many-to-one --> one order can have many products
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return round(total,2)

class ShippingAddress(models.Model):
    # attaching it to customer because if an order for some reason gets deleted, then we can have the shipping address for a customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.address

