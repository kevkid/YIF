from django.shortcuts import get_object_or_404, render
from .models import Image, Classes
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import random
# Create your views here.
def index(request):
    #lets get a random number going
    randNum = random.randint(0,Image.objects.count()-1)
    rand_img =  Image.objects.all()[randNum]
    cls = Classes.objects.all()
    context = {'randomImg' : rand_img, 'classes': cls}
    return render(request, 'web/index.html',context)#show the homePage
def survey(request):
    #lets get out choice
    try:
        selected_choice = 1#Classes.image_class_desc.get(pk=request.POST['survey'])
    except (KeyError, Classes.DoesNotExist):
        return render(request, 'web/index.html',{
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice += 1
        selected_choice.save()
        
    return HttpResponseRedirect(reverse('web:search', args=()))

def search(request, term):
    return render(request, 'web/search.html')#show the search page