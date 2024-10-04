from django.shortcuts import render
from rest_framework.decorators import api_view
from .services import SearchRepository

# Renders the search index page
def index(request):
    return render(request, 'search/index.html')

@api_view(['GET'])
def search_post(request):
    query_post_name = request.GET.get('post_name', '').strip()
    
    # Call repository method to get the filtered posts
    posts = SearchRepository.search_by_post_or_tag(query_post_name)
    
    return render(request, 'posts.html', {'posts': posts})
