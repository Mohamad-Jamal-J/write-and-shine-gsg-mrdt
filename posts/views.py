from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from accounts.models import User
from handlers import MessageHandler
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
                success_message = MessageHandler.get('post_created', False)
                messages.success(request, success_message)
                return redirect('get_posts')
            
            error_message = MessageHandler.get('invalid_data')
            messages.error(request, error_message)
            messages.error(request, "The post data is invalid")
            return redirect('get_posts')

        elif request.method == 'GET':
            # Render the form to create a post
            return render(request, 'posts/create_post.html')

    else:
        error_message = MessageHandler.get('not_logged')
        messages.error(request, error_message)
        return redirect('login_api')


@api_view(['GET'])
def get_posts(request):
    # Retrieve posts ordered by 'created_at' in descending order
    posts = Post.objects.all().order_by('-created_at')

    # Update post metadata
    posts = update_post_metadata(posts, request.user)

    return render(request, 'home.html', {'posts': posts})


@api_view(['GET'])
def get_user_posts(request, user_id):
    user = User.objects.filter(id=user_id).first() 
    if not user:
        error_message = MessageHandler.get('user_not_found')  
        messages.error(request, error_message)
        return redirect('get_posts') 
    
    posts = PostRepository.get_user_posts(user_id)
    posts = update_post_metadata(posts)

    return render(request, 'user.html', {'posts': posts, 'user': user})



@api_view(['GET', 'POST'])
def delete_edit_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=post_id).first() 
        if not post:
            error_message = MessageHandler.get('post_not_found')  
            messages.error(request, error_message)
            return redirect('get_posts') 

        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            error_message = MessageHandler.get('no_permission_to_edit')
            messages.error(request, error_message)
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
                success_message = MessageHandler.get('post_deleted', False)
                messages.success(request, success_message)
                return redirect('get_posts')  # Redirect to the list of posts after deletion  

            # Handle tag deletion
            if 'delete_tag' in request.POST:
                tag_id = request.POST['delete_tag']
                tag = Tag.objects.filter(id=tag_id)
                if not tag:
                    error_message = MessageHandler.get('tag_not_found')  
                    messages.error(request, error_message)
                    return redirect('get_posts') 
                
                post.tags.remove(tag) # Remove the tag from the post
                success_message = MessageHandler.get('tag_removed', False)
                messages.success(request, success_message) 
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
            
            success_message = MessageHandler.get('post_updated', False)
            messages.success(request, success_message)
            return redirect('get_posts') 

    error_message = MessageHandler.get('not_logged')
    messages.error(request, error_message)
    return redirect('login_api')


# added this variation of get_user_posts (we'll agree on/delete it later)
def get_user_posts_raw(request, user_id):
    user = User.objects.filter(id=user_id).first() 
    if not user:
        error_message = MessageHandler.get('user_not_found')  
        messages.error(request, error_message)
        return redirect('get_posts') 
    
    posts = Post.objects.filter(author=user)
    posts = update_post_metadata(posts)
    return {
        'posts': posts,
        'user': {
            'id': user.id,
            'name': user.name
        }
    }
