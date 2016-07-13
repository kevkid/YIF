import os
from web.models import Image, Classes
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf.urls.static import static
from imageFinder.settings import STATIC_URL, STATIC_IMAGES
from django.contrib.staticfiles.templatetags.staticfiles import static
import tools, web
# Create your views here.
def index(request):
    #lets get a random number going    
    return render(request, 'tools/index.html')#show the homePage


def ScanImages(request):
    allImages = list(Image.objects.values_list('image_location', flat=True))
    files = []
    fileRoots = []
    #path = STATIC_ROOT + 'web/images/'
    pth = web.__path__[0] + "/static/web/images"#os.path.join(tools.__path__,"static/web/images")
    for root, directories, filenames in os.walk(pth):#probably something wrong with the location
        for filename in filenames:
            files.append("images/" + filename)#temp, will need to chance            
            fileRoots.append(root)
            
    matches = set(allImages).intersection(set(files))#get the matches
    differenceDB_Matches = list(set(allImages) - (matches))
    #if not in the list of files delete the image...
    for item in differenceDB_Matches:
        #to reduce latency
        instance = Image.objects.get(image_location = item)
        instance.delete()
    #if in the file list and not in the matches add it to the db
    differenceFiles_Matches = list(set(files) - set(matches))
    for item in differenceFiles_Matches:
        #to reduce latency
        instance = Image(image_location=item)
        instance.save()
    return render(request, 'tools/ScanImages.html')#show the homePage
    #return HttpResponseRedirect(reverse('tools:ScanImages', args=()))
    

        