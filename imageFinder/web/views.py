from django.shortcuts import get_object_or_404, render
from .models import Image, Classes
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import random
from datetime import date

# Create your views here.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


def index(request):
    #lets get a random number going
    #randNum = random.randint(0,Image.objects.count()-1)
    #rand_img =  Image.objects.all()[randNum]
    cls = Classes.objects.all()
    import tools.retriever as retriever
    rand_img = retriever.getRandomDoc()
    if rand_img == -1:
        while rand_img != -1:
            rand_img = retriever.getRandomDoc()
    context = {'randomImg' : rand_img, 'classes': cls}
    return render(request, 'web/index.html',context)#show the homePage
def survey(request):
    #lets get out choice
    image = get_object_or_404(Image,id=request.POST['imageID'])
    
    try:
        #image_class = image.objects.get(pk=request.POST['survey'])
        s = request.POST['survey']#get from post
                
    except (KeyError, Classes.DoesNotExist):
        return render(request, 'web/index.html',{
            'error_message': "You didn't select a choice.",
        })
    else:
        #switch statement
        for case in switch(s):
            if case('0'):
                image.image_class_0 +=1
                break
            if case('1'):
                image.image_class_1 +=1
                break
            if case('2'):
                image.image_class_2 +=1
                break
            if case('3'):
                image.image_class_3 +=1
                break
            if case('4'):
                image.image_class_4 +=1
                break
            if case('5'):
                image.image_class_5 +=1
                break
            if case('6'):
                image.image_class_6 +=1
                break
            if case('7'):
                image.image_class_7 +=1
                break
            if case(): # default, could also just omit condition or 'if True'
                print ("No such choice")
                # No need to break here, it'll stop anyway
        if image.date_added == None:
            image.date_added = date.today()
        image.save()
        
        
    return HttpResponseRedirect(reverse('web:index', args=()))

def search(request):
    import tools.retriever as retriever
    
    images = retriever.SearchQuery(request.POST['searchTerm'])#"Shigella sonnei"
    if images != 0:
        context = {'searchImages' : images, 'imageCount' : len(images), 'term' : request.POST['searchTerm']}
    else:
        context = {'imageCount' : 0}
    return render(request, 'web/search.html', context)#show the search page