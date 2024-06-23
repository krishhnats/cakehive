from django.contrib import admin
from cakes.models import CakeCategory,Cake,ContactMessage
# Register your models here.
admin.site.register(CakeCategory)
admin.site.register(Cake)
admin.site.register(ContactMessage)
