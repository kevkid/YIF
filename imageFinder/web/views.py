from django.shortcuts import render
from .models import Image
import random
# Create your views here.
def index(request):
    #lets get a random number going
    randNum = random.randint(0,Image.objects.count()-1)
    rand_img =  Image.objects.all()[randNum]
    context = {'randomImg' : rand_img}
    return render(request, 'web/index.html',context)#show the homePage

def search(request, term):
    return render(request, 'web/search.html')#show the search page