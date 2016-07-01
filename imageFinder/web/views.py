from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request, 'web/index.html')#show the homePage

def search(request, term):
    return render(request, 'web/search.html')#show the search page