"""
URL configuration for cake_hive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cart import views
app_name="cart"
urlpatterns = [
    path('cartview', views.cartview, name="cartview"),
    path('addtocart/<int:p>',views.add_to_cart,name="addtocart"),
    path('remove/<int:p>',views.remove,name="remove"),
    path('delete/<int:p>', views.delete, name="delete"),
    path('place_order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orderview', views.orderview, name="orderview"),
    path('payment/success', views.payment_success, name='payment_success'),
    path('success_page', views.success_page, name='success_page'),
    path('razorpay_success', views.razorpay_success, name='razorpay_success'),

]
