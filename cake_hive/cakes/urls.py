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
from cakes import views
app_name="cakes"

urlpatterns = [
    path('', views.allcat, name="allcat"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

    path('viewcake/<int:p>', views.viewcake, name='viewcake'),
    path('details/<int:p>', views.details, name='details'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),

]
