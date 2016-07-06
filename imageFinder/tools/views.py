from django.shortcuts import render
import os
from .models import Image, Classes
from django.shortcuts import get_object_or_404, render

# Create your views here.
def index(request):
    #lets get a random number going
    
    return render(request, 'tools/index.html')#show the homePage
def ScanImages(request):
    files = []
    fileRoots = []
    for root, directories, filenames in os.walk('/web/static/web/images/'):
        for filename in filenames:
            image = get_object_or_404(Image,image_location=os.path.join(root,filename))
            if image is None:
                 image = Image(image)
            files.append(os.path.join(root,filename))
            
            fileRoots.append(root)
            
    