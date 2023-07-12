from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core import serializers
from django.db.models import Count, BooleanField, Case, When
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError

from .models import User, UserProfile, Post, Like, Following

page_number = None

def index(request):
    try: 
        posts_with_likes_count = Post.objects.annotate(likes_count=Count('liked_post'))
        all_posts = posts_with_likes_count.values('id', 'user__username', 'user__pk', 'content', 'date_time', 'likes_count').order_by('-date_time')

        page = paginator(request, all_posts)

        context = {
            'page': page
        }

        return render(request, 'network/index.html', context)
    except:
        return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def save_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        try:
            post = Post()
            post.user = request.user
            post.content = content

            post.save()

            return HttpResponseRedirect(reverse("index"))
        except:
            raise Http404('Could not save post.')


def get_all_posts(request):
    try:
        all_posts = Post.objects.all()

        return render(request, "network/index.html", {
            'all_posts': all_posts,
        })
    except:
        raise HttpResponseServerError('Could not get any posts.')


def profile(request, id, follow = None):
    try:
        user = User.objects.get(pk = id)

        its_user = False
        follows = False

        if request.user.is_authenticated:

            if(request.user.pk == id):
                its_user = True

            if(follow == 'True'):
                add_following = Following()
                add_following.user = request.user
                add_following.user_follows = user
                add_following.save()
            elif(follow == 'False'):
                Following.objects.filter(user = request.user, user_follows = user).delete()

            if(Following.objects.filter(user = request.user, user_follows = user)):
                follows = True

        following = Following.objects.filter(user = id).count()
        followers = Following.objects.filter(user_follows = id).count()

        posts_with_likes_count = Post.objects.filter(user = user).annotate(likes_count=Count('liked_post')).order_by('-date_time')
        user_posts = posts_with_likes_count.values('id', 'user__username', 'user__pk', 'content', 'date_time', 'likes_count')

        page = paginator(request, user_posts)

        return render(request, "network/profile.html", {
            'user': user,
            'its_user': its_user,
            'following': following,
            'follows': follows,
            'followers': followers,
            'page': page
        })
    except:
        raise HttpResponseServerError('Could not load user profile.') 


@login_required
def save_edited_post(request, id):
    try:
        if request.method == 'PUT':

            result = request.body.decode()
            result_object = json.loads(result)

            editedPost = get_object_or_404(Post, pk = id)
            editedPost.content  = result_object['editedPost']

            editedPost.save()

            response_data = {
                'message': 'Post successfully updated'
            }

            return JsonResponse(response_data, status=200)
    except:
        raise HttpResponseServerError('Could not save edited post.') 


@login_required
def liked(request, id):
    try:
        if request.method == 'POST':

            result = request.body.decode()
            result_object = json.loads(result)
            
            liked_post = Post.objects.get(pk = id)

            if(result_object['action'] == 'liked'):
                liked = Like()
                liked.post = liked_post
                liked.user = request.user

                liked.save()
            else:
                Like.objects.get(post = liked_post, user = request.user).delete()

            liked_count = Like.objects.filter(post = liked_post).count()

            response_data = {
                'message': 'Post successfully updated',
                'liked_count': liked_count
            }

            return JsonResponse(response_data, status=200) 
    except:
        raise HttpResponseServerError('Could not manage like actions.')


@login_required
def liked_posts(request, path):
    try:
        if path == 'index':
            posts_with_likes_count = Post.objects.annotate(likes_count=Count('liked_post'), liked_by_user=Case(
                    When(liked_post__user=request.user, then=True),
                    default=False,
                    output_field=BooleanField()
            )).order_by('-date_time')
        else:
            if path == 'following':
                user_ids = Following.objects.filter(user=request.user).values_list('user_follows_id', flat=True)
            else:
                user_ids = path[-1]

            posts_with_likes_count = Post.objects.filter(user__id__in=user_ids).annotate(likes_count=Count('liked_post'), liked_by_user=Case(
                    When(liked_post__user=request.user, then=True),
                    default=False,
                    output_field=BooleanField())).order_by('-date_time')

        all_posts = posts_with_likes_count.values('id', 'liked_by_user')

        paginator = Paginator(all_posts, 10)

        global page_number
        pg_number = page_number
        page_posts = paginator.get_page(pg_number).object_list    

        posts_list = list(page_posts)

        response_data = {
            'message': 'success',
            'all_posts': posts_list
        }

        return JsonResponse(response_data, status=200)
    except:
        response_data = {
            'message': 'Error occured'
        }

        return JsonResponse(response_data, status=500)


@login_required
def following(request):
    try:
        following_user_ids = Following.objects.filter(user=request.user).values_list('user_follows_id', flat=True)

        following_posts = Post.objects.filter(user__id__in=following_user_ids).annotate(likes_count=Count('liked_post')).order_by('-date_time')

        page = paginator(request, following_posts)

        return render(request, "network/following.html", {
            'page': page
        })
    except:
        raise HttpResponseServerError('Could not load following page.') 


def paginator(request, posts):
    try:
        paginator = Paginator(posts, 10)

        global page_number
        page_number = request.GET.get('page', '1')  
        page = paginator.get_page(page_number)

        return page
    except:
        raise Http404('Could not load page.') 
    