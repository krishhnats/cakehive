from django import forms
from .models import Orders

class OrderForm(forms.Form):
    shipping_address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=True)
    PAYMENT_METHOD_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Razorpay', 'Razorpay'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, required=True)
