from django.shortcuts import render
from .models import Image
# Create your views here.
def index(request):
    
    rand_img =  Image.objects.first()
    return render(request, 'web/index.html')#show the homePage

def search(request, term):
    return render(request, 'web/search.html')#show the search page