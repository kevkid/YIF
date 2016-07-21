from django.shortcuts import get_object_or_404, render
from .models import Image, Classes
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import random
from datetime import date

import lucene, os, web
from java.io import File, Reader, StringReader

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField,StringField

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader, IndexWriter, IndexWriterConfig, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

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
    rand_img, img_id = retriever.getRandomDoc()
    if rand_img == -1:
        while rand_img == -1:
            rand_img = retriever.getRandomDoc()
    
    context = {'randomImg' : rand_img, 'classes': cls, 'img_id': img_id}
    return render(request, 'web/index.html',context)#show the homePage
def survey(request):
    #lets get out choice
    location = web.__path__[0] + "/static/web/files/index/index.figures"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    
        
    try:
        #image_class = image.objects.get(pk=request.POST['survey'])
        s = request.POST['survey']#get from post
        
                
    except (KeyError, Classes.DoesNotExist):
        return render(request, 'web/index.html',{
            'error_message': "You didn't select a choice.",
        })
    else:
        #switch statement
        image_class = ""
        for case in switch(s):
            if case('0'):
                image_class += "0"
                break
            if case('1'):
                image_class += "1"
                break
            if case('2'):
                image_class += "2"
                break
            if case('3'):
                image_class += "3"
                break
            if case('4'):
                image_class += "4"
                break
            if case('5'):
                image_class += "5"
                break
            if case('6'):
                image_class += "6"
                break
            if case('7'):
                image_class += "7"
                break
            if case(): # default, could also just omit condition or 'if True'
                print ("No such choice")
                # No need to break here, it'll stop anyway
        docNum = request.POST['imageID']#get document id
        doc = reader.document(int(docNum))
        fname = doc.get("filename")
        print(fname)
        #SimpleFSDirectory(File(location)).clearLock(IndexWriter.WRITE_LOCK_NAME);
        fileClassField = doc.get("Classification")
        fileClassField = str(fileClassField) + ", " + image_class
        doc.removeField("Classification")
        
        doc.add(StringField("Classification", fileClassField, Field.Store.YES))
        t = doc.get("Classification")
        indexDir = SimpleFSDirectory(File(location))
        writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, StandardAnalyzer())
        writer = IndexWriter(indexDir, writerConfig)
        writer.updateDocument(Term("filename", fname), doc)#If field exists update
        writer.close()
        #writer.unlock(SimpleFSDirectory(File(location)))
        
    return HttpResponseRedirect(reverse('web:index', args=()))

def search(request):
    import tools.retriever as retriever
    
    images = retriever.SearchQuery(request.POST['searchTerm'])#"Shigella sonnei"
    if images != 0:
        context = {'searchImages' : images, 'imageCount' : len(images), 'term' : request.POST['searchTerm']}
    else:
        context = {'imageCount' : 0}
    return render(request, 'web/search.html', context)#show the search page