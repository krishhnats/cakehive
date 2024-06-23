from cakes.models import CakeCategory

def links(request):
    c=CakeCategory.objects.all()
    return { 'links':c }