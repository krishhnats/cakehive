from django.db import models
from cakes.models import Cake
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    user_entry_date = models.DateField(null=True, blank=True)
    user_notes = models.TextField(null=True, blank=True)

    def subtotal(self):
        return self.quantity*self.cake.price

    def __str__(self):
        return self.cake.name

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, null=True, blank=True)
    no_of_items = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.TextField()
    phone = models.BigIntegerField()
    payment_method = models.CharField(max_length=50)
    order_status = models.CharField(max_length=30, default="pending")
    delivery_status = models.CharField(max_length=30, default="pending")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user_entry_date = models.DateField(null=True, blank=True)
    paid=models.BooleanField(default=False)
    is_delivered=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_delivered:
            self.delivery_status = "delivered"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username




