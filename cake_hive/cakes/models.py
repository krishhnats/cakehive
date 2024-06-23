from django.db import models

class CakeCategory(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    image = models.ImageField(upload_to='categories', blank=True, null=True)

    def __str__(self):
        return self.name



class Cake(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='cakes', null=True, blank=True)
    desc = models.TextField()
    weight = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available = models.BooleanField(default=True)
    user_entry_date = models.DateField(null=True, blank=True)  # Field for users to enter a date
    user_notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CakeCategory, on_delete=models.CASCADE, related_name='cakes')

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name