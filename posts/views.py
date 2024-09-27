from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from posts.models import Post, Post_Tag, Tag
from posts.serializers import PostSerializer

# Create your views here.
def index(request):
    return render(request, 'posts/index.html')  
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  # The user clicked the button to create a post
            title = request.POST.get('title')
            body = request.POST.get('body')
            tags = request.POST.getlist('tags')

            if title and body:
                post = Post.objects.create(
                    title=title,
                    body=body,
                    author=request.user  # Set the logged-in user as the author
                )

                for tag_name in tags:
                    tag_name = tag_name.strip().capitalize()  # Capitalize the first letter and trim whitespace
                    tag, created = Tag.objects.get_or_create(name=tag_name)  # Check for existing tag or create a new one
                    Post_Tag.objects.create(post=post, tag=tag)  # Link the tag to the post

                return HttpResponse("Post created successfully!")
                # If we want to return the home page
                # return redirect('home')

            return HttpResponse("The post data is not valid", status=400)

        elif request.method == 'GET':
            # The page that should appear to the user and they should fill the form in it to create the post
            return render(request, 'create_post.html')
            # return HttpResponse("Form to be filled by user")
    else:
        return HttpResponse("You should be logged in to create a post", status=403)