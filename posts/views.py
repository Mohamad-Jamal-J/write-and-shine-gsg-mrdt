from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from posts.models import  Post, Tag
from django.utils import timezone


def index(request):
    return render(request, 'posts/index.html')  

def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  # The user clicked the button to create a post
            title = request.POST.get('title')
            body = request.POST.get('body')
            tags_input = request.POST.get('tags')  # Get the tags input as a single string
            
            # Split the tags by comma and strip whitespace
            tags = [tag.strip().capitalize() for tag in tags_input.split(',') if tag.strip()]

            if title and body:
                post = Post.objects.create(
                    title=title,
                    body=body,
                    author=request.user  # Set the logged-in user as the author
                )

                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)  # Get or create the tag
                    post.tags.add(tag)  # Associate the tag with the post using the ManyToManyField

                return redirect('get_posts')  
                # If you want to redirect to the home page:
                # return redirect('home')

            return HttpResponse("The post data is not valid", status=400)

        elif request.method == 'GET':
            # The form to create the post
            return render(request, 'create_post.html')

    else:
        return HttpResponse("You should be logged in to create a post", status=403)


@api_view(['GET', 'POST'])
def delete_edit_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            return Response({"message": "You do not have permission to edit or delete this post."}, status=403)

        if request.method == 'GET':
            # Handle the edit action
            if 'edit' in request.GET:
                return render(request, 'post_edit.html', {'post': post})
            else:
                return render(request, 'posts.html', {'post': post})

        elif request.method == 'POST':
            # Check if the form indicates deletion
            if 'delete' in request.POST:
                post.delete()  # Delete the post
                return redirect('get_posts')  # Redirect to the list of posts after deletion  

            # Handle tag deletion
            if 'delete_tag' in request.POST:
                tag_id = request.POST['delete_tag']
                tag = get_object_or_404(Tag, pk=tag_id)
                post.tags.remove(tag)  # Remove the tag from the post
                return redirect('get_posts')  # Redirect to the list of posts after deleting a tag

            # Handle adding new tags
            new_tag_name = request.POST.get('new_tag', '').strip()
            if new_tag_name:
                tag, created = Tag.objects.get_or_create(name=new_tag_name.capitalize())
                post.tags.add(tag)  # Associate the new tag with the post

            # Handle the post editing
            post_fields = ['title', 'body']
            for field in post_fields:
                if field in request.POST and request.POST[field] != '':
                    setattr(post, field, request.POST[field])
            post.updated_at = timezone.now()
            post.save()
            
            return redirect('get_posts') 

    return HttpResponse("You should be logged in to delete/edit a post", status=403)
