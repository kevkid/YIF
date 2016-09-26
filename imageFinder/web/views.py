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
from pandas.tslib import fields

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
    rand_img, img_id = retriever.getRandomDocOfCertainClass()
    if rand_img == -1:
        while rand_img == -1:
            rand_img = retriever.getRandomDocOfCertainClass()
    
    context = {'randomImg' : rand_img, 'classes': cls, 'img_id': img_id}
    return render(request, 'web/index.html',context)#show the homePage
def survey(request):
    ipAddr = get_client_ip(request)
    instances = (Classes.objects.values_list('image_class_desc'))
    instances = [i[0] for i in instances]
    #cnt = len(instances)
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
        image_class = instances[int(s)]
        docNum = request.POST['imageID']#get document id
        doc = reader.document(int(docNum))
        fname = doc.get("filename")
        print(fname)
        #SimpleFSDirectory(File(location)).clearLock(IndexWriter.WRITE_LOCK_NAME);
        fileClassField = doc.get("Classification")
        if str(fileClassField) == "None":#check if the field exists####NEED TO CHECK THIS
            fileClassField = str(ipAddr + ":" + image_class)#I think we must add an ip address to this
        else:
            fileClassField = str(ipAddr + ":" + fileClassField) + ", " + image_class
            
        #doc.removeField("Classification")
        
        #doc.add(StringField("Classification", fileClassField, Field.Store.YES))
        #t = doc.get("Classification")
        #reader.close()
        indexDir = SimpleFSDirectory(File(location))
        writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, StandardAnalyzer())
        writer = IndexWriter(indexDir, writerConfig)
        fields = doc.getFields()#get all fields
        doc2 = Document()
        classificationFieldFlag = False
        for f in fields:
            field = Field.cast_(f)
            (k, v) = field.name(), field.stringValue()
            if k == "Classification":
                classificationFieldFlag = True
                field = StringField("Classification", fileClassField, Field.Store.YES)
                doc2.add(field)
            else:
                doc2.add(field)

        if classificationFieldFlag == False:#this does not exist in the document must add
            doc2.add(StringField("Classification", fileClassField, Field.Store.YES))
#         doc2.add(StringField("Classification", fileClassField, Field.Store.YES))
#         doc2.add(StringField("fid", doc.get("fid"), Field.Store.YES))
#         doc2.add(StringField("articleid", doc.get("articleid"), Field.Store.YES))
#         doc2.add(StringField("caption", doc.get("caption"), Field.Store.YES))
#         doc2.add(StringField("figureid", doc.get("figureid"), Field.Store.YES))
#         doc2.add(StringField("filename", doc.get("filename"), Field.Store.YES))
#         doc2.add(StringField("filepath", doc.get("filepath"), Field.Store.YES))
#         doc2.add(StringField("label", doc.get("label"), Field.Store.YES))
        
        #writer.updateDocument(Term("fid","f000000000023"), doc2)#If field exists update
        writer.updateDocument(Term("fid", doc.get("fid")), doc2)#If field exists update
        writer.commit();
        #writer.optimize()
        writer.close()
        #writer.unlock(SimpleFSDirectory(File(location)))
        
    return HttpResponseRedirect(reverse('web:index', args=()))

def search(request):
    import tools.retriever as retriever
    cls = Classes.objects.all()
    advSearch = request.POST.getlist('advSearch')
    classes = request.POST.get('classes')
    try:
        
        (images, pmcids,titles) = retriever.SearchQuery(request.POST['searchTerm'], advSearch, classes)#"Shigella sonnei"
    except:
        #something went wrong with getting the images, set to 0 and give 0 results
        images = 0
    
    if images != 0:
        context = {'searchImages' : zip(images,pmcids,titles), 'imageCount' : len(images),
                    'term' : request.POST['searchTerm'], 'classes': cls, 'advSearch' : ', '.join(advSearch)}
    else:
        context = {'imageCount' : 0, 'classes': cls, 'term' : request.POST['searchTerm'], 'advSearch' : ', '.join(advSearch)}
    return render(request, 'web/search.html', context)#show the search page

def OpenDocument(request):
    import tools.retriever as retriever
    import tools.related_images as related_images
    cls = Classes.objects.all()

    (abstract, doi, title, volume, year, publisher, fullText, pdf,pmcid) = retriever.getDocumentPMC_ID(request.GET['pmcid'],0)
    relatedDocs = related_images.getRelatedArticles(pmcid)
    context = {'abstract':abstract, 'doi':doi, 'volume':volume, 
               'year':year, 'publisher':publisher, 'fullText':fullText, 'pdf':pdf, 'title':title,
               'img_loc' : request.GET['img_loc'], 'classes': cls, 'relatedDocs':relatedDocs}#we should be getting the article id and then searching for the image via this
    return render(request, 'web/opendocument.html', context)#show the search page

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    