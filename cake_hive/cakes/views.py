from django.shortcuts import render,get_object_or_404
from cakes.models import CakeCategory,Cake
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from cakes.forms import ContactForm


def allcat(request):
    c=CakeCategory.objects.all()
    return render(request, 'allcat.html',{'c':c})

def viewcake(request,p):
    c=CakeCategory.objects.get(id=p)
    v=Cake.objects.filter(category=c)
    return render(request,'viewcake.html',{'c':c,'v':v})



def details(request, p):
    v = Cake.objects.get(id=p)
    return render(request, 'details.html', {'v': v})


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been submitted successfully.')
            form = ContactForm()  # Reset the form for the next submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']

        if (cp == p):
            user = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            user.save()
            return redirect('cakes:login')
        else:
            return HttpResponse("passwords are not the same")

    return render(request, 'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('cakes:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')



def user_logout(request):
    logout(request)
    return allcat(request)


