import sys
import lucene, os, web
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from string import replace

def SearchQuery(queryString): 
    #if __name__ == "__main__":
    #if __name__ == "retriever":
        location = web.__path__[0] + "/static/web/files/index/index.articles"
        lucene.initVM()
        analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
        reader = IndexReader.open(SimpleFSDirectory(File(location)))
        searcher = IndexSearcher(reader)
     
        query = QueryParser(Version.LUCENE_4_10_1, "keywords", analyzer).parse(queryString)#"Shigella sonnei"
        MAX = 1000
        hits = searcher.search(query, MAX)
     
        print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
        paths = []
        for hit in hits.scoreDocs:
            #print hit.score, hit.doc, hit.toString()
            doc = searcher.doc(hit.doc)
            #print doc.get("articlepath")
            paths.append(doc.get("articlepath"))
        
        files = []
        fileRoots = []
        #path = STATIC_ROOT + 'web/images/'
        pth = paths[0].replace("/home/kevin/Downloads/","/home/kevin/git/YIF/imageFinder/web/static/web/")#os.path.join(tools.__path__,"static/web/images")
        for root, directories, filenames in os.walk(pth):#probably something wrong with the location
            for filename in filenames:
                if (".jpg" or ".gif" or ".png") in filename:
                    files.append(root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/","") + "/" +filename)#temp, will need to chance            
                    fileRoots.append(root)
                    print (root.replace("/home/kevin/git/YIF/imageFinder/web/static/web/","") + "/" + filename)
                    
        return files            
