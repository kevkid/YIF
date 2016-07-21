import lucene, os, web
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def updateIndex():
    
    location = web.__path__[0] + "/static/web/files/index/index.articles"
    SimpleFSDirectory indexDir = SimpleFSDirectory(File(location))
    IndexWriter writer = new IndexWriter(indexDir,new StandardAnalyzer, False);#update it
    #*:* AND -myfield:[* TO *]
    if 
    writer.UpdateDocument(new Term("Classification",image_class), doc);