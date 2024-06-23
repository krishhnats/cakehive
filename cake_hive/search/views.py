from django.shortcuts import render
from cakes.models import Cake
from django.db.models import Q
# Create your views here.
def searchcake(request):
    if(request.method=="POST"):
        v=None
        q=""
        query=request.POST['q']
        if(query):
            v=Cake.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
            q = query
    return render(request,"search.html",{'v':v,'q':q})