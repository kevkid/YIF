import tools.retriever as retriever
import sys
import lucene, os, web
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher, BooleanClause, BooleanQuery
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser, QueryParserBase
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.queries.mlt import MoreLikeThis



def getRelatedArticles(pmcid):
    location = web.__path__[0] + "/static/web/files/index/index.articles"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    searcher = IndexSearcher(reader)
    q = MultiFieldQueryParser(Version.LUCENE_4_10_1, ["pmcid"], analyzer)
        #query.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    q = MultiFieldQueryParser.parse(q, pmcid)
    MAX = 10000
    hits = searcher.search(q, MAX)
    id = hits.scoreDocs[0].doc#searcher.doc(hits[0].scoredocs[0].doc)
    
    
    result = BooleanQuery()
    result.add(BooleanClause(q, BooleanClause.Occur.MUST_NOT))
    
    
    titlemlt = getSimilarityGenerator("title", 1, 1, 2)
    abstractmlt = getSimilarityGenerator("abstract", 2, 5, 2)
    citationmlt = getSimilarityGenerator("citation", 2, 5, 2)
    fulltextmlt = getSimilarityGenerator("fulltext", 2, 5, 2)
    keywordmlt = getSimilarityGenerator("keyword", 1, 1, 1)   
    
    titleQ = titlemlt.like(id);
    titleQ.setBoost(0.2)
    abstractQ = abstractmlt.like(id);
    abstractQ.setBoost(0.1);

    #Do we even want to include a query for similar citations?
    citationQ = citationmlt.like(id);
    citationQ.setBoost(0.0);

    fulltextQ = fulltextmlt.like(id);
    fulltextQ.setBoost(0.0);

    keywordQ = keywordmlt.like(id);
    keywordQ.setBoost(0.0);


    result.add(BooleanClause(titleQ, BooleanClause.Occur.SHOULD));
    result.add(BooleanClause(abstractQ, BooleanClause.Occur.SHOULD));
    result.add(BooleanClause(citationQ, BooleanClause.Occur.SHOULD));
    result.add(BooleanClause(fulltextQ, BooleanClause.Occur.SHOULD));
    result.add(BooleanClause(keywordQ, BooleanClause.Occur.SHOULD));
    
    hits = searcher.search(result, 5)
    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, result)
    paths = []
    pmcids = []
    titles = []
    files = []
    for hit in hits.scoreDocs:
            #print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
            #print doc.get("articlepath")
        paths.append(doc.get("articlepath"))#get both the article path and the pmcid
        pmcids.append( doc.get("pmcid"))
        titles.append( doc.get("title"))
        #if len(hits.scoreDocs) > 0:
        files.append(retriever.get_image(paths))
    #    // Do we want to play around with result.setMinimumNumberShouldMatch(n)
    #    // to filter results?
    files = [val for sublist in files for val in sublist]
    return zip(titles, files);
    
def getSimilarityGenerator(field,minTermFreq,minDocFreq,minWordLen): # maxQueryTerms as parameter
    maxQueryTerms = 30
    location = web.__path__[0] + "/static/web/files/index/index.articles"
    #lucene.initVM()
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    reader = IndexReader.open(SimpleFSDirectory(File(location)))
    
    simil = MoreLikeThis(reader)
    simil.setFieldNames(field)
    simil.setMinTermFreq(minTermFreq)
    simil.setMinDocFreq(minDocFreq)
    simil.setMinWordLen(minWordLen)

    #Use same maxQueryTerms to prevent longer queries
    simil.setMaxQueryTerms(maxQueryTerms)

    simil.setBoost(True) #!Boost terms within queries by tf-idf score
    return simil
    
    