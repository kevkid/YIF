import sys
import lucene, os, web
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser, QueryParserBase
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from string import replace
from _random import Random
from random import randrange
from pylint.pyreverse.utils import ABSTRACT

def SearchQuery(queryString, fields, classification): 
    #if __name__ == "__main__":
    #if __name__ == "retriever":
    location = web.__path__[0] + "/static/web/files/index/index.articles"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    #multi field query: http://stackoverflow.com/questions/2005084/how-to-specify-two-fields-in-lucene-queryparser
    
    query = MultiFieldQueryParser(Version.LUCENE_4_10_1, fields, analyzer)
    #query.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    query = MultiFieldQueryParser.parse(query, queryString)
    #query.parse(queryString)#"Shigella sonnei"
    #query = QueryParser(Version.LUCENE_4_10_1, "abstract", analyzer).parse(queryString)#"Shigella sonnei"

    MAX = 10000
    hits = searcher.search(query, MAX)
 
    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
    paths = []
    pmcids = []
    titles = []
    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        pmcids.append(doc.get("pmcid"))
    
        
    images = get_image_pmcid(pmcids, classification)#should take in pmcids and class
    doc_img_paths = []
    for img in images:
        imgClass = img.get("class")
        if imgClass == classification or classification == "all":
            doc_img_paths.append(img.get("filepath") + "/" + img.get("figureid"))#get both the article path and the pmcid
            pmcids.append( doc.get("pmcid"))
            titles.append( doc.get("title"))
    paths.append(doc_img_paths[0])#append the list of paths for the images for each article, only first image
    files = paths
    return files, pmcids, titles
        
def getRandomDocOfCertainClass():
        classes = [1,3]#temporary classes, we will set this later
        location = web.__path__[0] + "/static/web/files/index/index.figures"
        #lucene.initVM()
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        
        docAndID = getDocumentClass(classes)#get document from these classes
        if docAndID == -1:
            while docAndID == -1:
                docAndID = getDocumentClass(classes)
        doc = docAndID[0]
        docNum = docAndID[1] 
        fileName = doc.get("filename")
        filePath = doc.get("filepath")
            
        result = filePath + "/" + fileName 
        result = result.replace("/home/kevin/Downloads/","/")
        return (result, docNum)
def getRandomDoc():
    
        location = web.__path__[0] + "/static/web/files/index/index.figures"
        #lucene.initVM()
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
        reader = IndexReader.open(SimpleFSDirectory(File(location)))
        searcher = IndexSearcher(reader)
     
        #query = QueryParser(Version.LUCENE_4_10_1, "keywords", analyzer).parse(queryString)#"Shigella sonnei"
        MAX = 1000
        docNum = randrange(0, reader.maxDoc())
        doc = reader.document(docNum)
        
        fileName = doc.get("filename")
        filePath = doc.get("filepath")
            
        result = filePath + "/" + fileName 
        result = result.replace("/home/kevin/Downloads/","/")
        return (result, docNum)
        
#getRandomDoc()

def getRandomDoc2():
    
        location = web.__path__[0] + "/static/web/files/index/index.articles"
        #lucene.initVM()
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
        reader = IndexReader.open(SimpleFSDirectory(File(location)))
        searcher = IndexSearcher(reader)
     
        #query = QueryParser(Version.LUCENE_4_10_1, "keywords", analyzer).parse(queryString)#"Shigella sonnei"
        MAX = 1000
        docNum = randrange(0, reader.maxDoc())
        doc = reader.document(docNum)
     
        #print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
        files = []
        fileRoots = []
        paths = []
        paths.append(doc.get("articlepath"))
        pth = paths[0].replace("/home/kevin/Downloads/","/home/kevin/git/YIF/imageFinder/web/static/web/")#os.path.join(tools.__path__,"static/web/images")
        for root, directories, filenames in os.walk(pth):#probably something wrong with the location
            for filename in filenames:
                if (".jpg" or ".gif" or ".png") in filename:
                    files.append(root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/","") + "/" +filename)#temp, will need to chance            
                    fileRoots.append(root)
                    print (root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/","") + "/" + filename)
        try: 
            rng = randrange(0, len(files))
        except:
            return -1
        else:
             return files[randrange(0, len(files))]

def getDocumentPMC_ID(pmcid, imageAndTitle = 0):
    location = web.__path__[0] + "/static/web/files/index/index.articles"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    #multi field query: http://stackoverflow.com/questions/2005084/how-to-specify-two-fields-in-lucene-queryparser
    query = QueryParser(Version.LUCENE_4_10_1, "pmcid", analyzer).parse(pmcid)#"Shigella sonnei"
    MAX = 1000
    hits = searcher.search(query, MAX)
    title = ""
    abstract = ""
    fullText = "http://www.ncbi.nlm.nih.gov/pmc/articles/" + pmcid + "/"
    doi = ""#need to split
    
    volume = ""
    year = ""
    publisher = ""
    for hit in hits.scoreDocs:#should only be one
        #print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        if(imageAndTitle == 1):
            paths = []
            paths.append(doc.get("articlepath"))
            image = get_image(paths)
            
        abstract = doc.get("abstract")
        doi = doc.get("doi")
        title = doc.get("title")
        volume = doc.get("volume")
        year = doc.get("year")
        publisher = doc.get("publisher")
    if doi is not None:
        doiSecond = doi.split('/')
        doiSecond = doiSecond[1]#second part
    else:
        doiSecond = ""
    #http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3363814/pdf/cc11003.pdf
    pdf = "http://www.ncbi.nlm.nih.gov/pmc/articles/" + pmcid + "/pdf/" + doiSecond + ".pdf" 
    if(imageAndTitle == 1):
        return title, image, pmcid#image may sometimes show up    
    else:
        return abstract, doi, title, volume, year, publisher, fullText, pdf,pmcid#image may sometimes show up


def getDocumentClass(reqClass):
    import random
    location = web.__path__[0] + "/static/web/files/index/index.figures"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    #multi field query: http://stackoverflow.com/questions/2005084/how-to-specify-two-fields-in-lucene-queryparser
    query = QueryParser(Version.LUCENE_4_10_1, "class", analyzer).parse(str(random.choice(reqClass)))#get random class and search for a document from here
    MAX = 1000
    hits = searcher.search(query, MAX)
    docs = []
    for hit in hits.scoreDocs:#should only be one
        #print hit.score, hit.doc, hit.toString()
        docs.append((searcher.doc(hit.doc), hit.doc))
    
    if not docs:
        return -1
    else:
        doc = random.choice(docs)
        return doc#return document and ID

def get_image(paths):
    files = []
    for pth in paths:
        fileRoots = []
        # path = STATIC_ROOT + 'web/images/'
        pth = pth.replace("/home/kevin/Downloads/", "/home/kevin/git/YIF/imageFinder/web/static/web/")  # os.path.join(tools.__path__,"static/web/images")
        for root, directories, filenames in os.walk(pth):  # probably something wrong with the location
            for filename in filenames:
                if (".jpg" or ".gif" or ".png") in filename:
                    files.append(root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/", "") + "/" + filename)  # temp, will need to chance            
                    fileRoots.append(root)
                    print (root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/", "") + "/" + filename)
                    break  # exit from loop
    return files
def get_image_pmcid(pmcid, classes = ""):
    fields = ["pmcid", "class"]
    docs = []
    location = web.__path__[0] + "/static/web/files/index/index.figures"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    # multi field query: http://stackoverflow.com/questions/2005084/how-to-specify-two-fields-in-lucene-queryparser
    
    #query = MultiFieldQueryParser(Version.LUCENE_4_10_1, fields, analyzer)
    # query.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    
    #query = query.parse(query, ('4175339','1'))
    # query.parse(queryString)#"Shigella sonnei"
    # query = QueryParser(Version.LUCENE_4_10_1, "abstract", analyzer).parse(queryString)#"Shigella sonnei"

    MAX = 10000
    #hits = searcher.search(query, MAX)
    if classes == "all":
        queryStr = "pmcid:(" + ' '.join(pmcid) +")"
    else:
        queryStr = "pmcid:(" + ' '.join(pmcid) +")" + " AND class:" + classes
    query = QueryParser(Version.LUCENE_4_10_1, "pmcid",analyzer)#needed to build a custom query
    q = query.parse(queryStr) 
    hits = searcher.search(q, MAX)
    for hit in hits.scoreDocs:#should only be one
        #print hit.score, hit.doc, hit.toString()
        docs.append(searcher.doc(hit.doc))
    return docs #This will return the image documents that belong to a pmcid(article)
