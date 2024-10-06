from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from accounts.models import User
from posts.models import Post, Tag
from django.utils import timezone
from django.contrib import messages
from posts.services import PostRepository
from posts.services import update_post_metadata


@api_view(['POST', 'GET'])
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  # The user clicked the button to create a post
            title = request.POST.get('title')
            body = request.POST.get('body')
            tags_input = request.POST.get('tags')  # Get the tags input as a single string
            
            # Split the tags by comma and strip whitespace
            tags = [tag.strip().capitalize() for tag in tags_input.split(',') if tag.strip()]

            if title and body:
                PostRepository.create_post(title, body, request.user, tags)
                return redirect('get_posts')

            messages.error(request, "The post data is invalid")
            return redirect('get_posts')

        elif request.method == 'GET':
            # Render the form to create a post
            return render(request, 'posts/create_post.html')

    else:
        messages.error(request, "You should have an account and be logged in to create a post")
        return redirect('login_api')


@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()

    # Update post metadata
    posts = update_post_metadata(posts)

    return render(request, 'home.html', {'posts': posts})


@api_view(['GET'])
def get_user_posts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = PostRepository.get_user_posts(user_id)
    posts = update_post_metadata(posts)

    return render(request, 'user.html', {'posts': posts, 'user': user})



@api_view(['GET', 'POST'])
def delete_edit_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            messages.error(request, "You do not have permission to edit or delete this post")
            return redirect('get_posts')

        if request.method == 'GET':
            # Handle the edit action
            if 'edit' in request.GET:
                return render(request, 'posts/edit_page.html', {'post': post})
            else:
                return render(request, 'home.html', {'post': post})

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

    messages.error(request, "You should be logged in to delete/edit a post")
    return redirect('login_api')


# added this variation of get_user_posts (we'll agree on/delete it later)
def get_user_posts_raw(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user)
    posts = update_post_metadata(posts)
    return {
        'posts': posts,
        'user': {
            'id': user.id,
            'name': user.name
        }
    }
