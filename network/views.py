from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

from django.http import HttpResponse, JsonResponse, Http404

from .models import User, UserProfile, Post


def index(request):
    try: 
        all_posts = Post.objects.all().order_by('-date_time')

        return render(request, "network/index.html", {
            'all_posts': all_posts,
        })
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
            raise e  #handle error logic


def get_all_posts(request):
    try:
        all_posts = Post.objects.all()

        return render(request, "network/index.html", {
                'all_posts': all_posts,
        })
        # all_posts = serializers.serialize('json', all_posts)
        
        # return HttpResponse(all_posts)
    except:
        raise Http404('Could not get any posts.')