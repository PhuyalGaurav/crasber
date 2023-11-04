from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect,JsonResponse
from itertools import chain
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



from .models import User, Post
LOGIN_URL = '/login'
MAX_POSTS = 10

def error(request, message):
    return render(request, "network/error.html", {
        "message" : message
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def index(request):
    posts = Post.objects.all().order_by('-creation_date')

    #paginations 

    paginator = Paginator(posts, MAX_POSTS)
    page = request.GET.get('page')
    posts_paginator = paginator.get_page(page)
    
    return render(request, "network/index.html",{
       "posts" : posts,
       "page" : posts_paginator,
    })


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def newposter(request):
    if request.method == "POST":
        if is_ajax(request):
            text = json.load(request)['post_content']
            if not text:
                return error(request, "Must provide a content")
            thisPost = Post(user=request.user, content=text)
            thisPost.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return error(request, "No Hacking in my site baby")
    else:
      return error(request, "Not This Way Baby")
    
def newpost(request):
    return render(request, "network/newpost.html")

@login_required(login_url=LOGIN_URL )
def userpage(request, user_id ):
    requested_user = User.objects.get(id=user_id)
    logged_user = User.objects.get(id= request.user.id)
    if request.method  == "GET":
        posts = Post.objects.filter(user=user_id).order_by('-creation_date')
        if request.user.id == user_id:
            show_follow = False
        else:
            show_follow = True
        logged_following_list = logged_user.following.split(",")
        if str(user_id) in  logged_following_list:
            is_following = True
        else:
            is_following = False
        paginator = Paginator(posts, MAX_POSTS)
        page = request.GET.get('page')
        posts_paginator = paginator.get_page(page)
        return render(request, "network/userpage.html",{
            "username" : requested_user.username,
            "posts" : posts,
            "followers" : len(requested_user.follower.split(",")),
            "following" : len(requested_user.following.split(",")),
            "is_following" : is_following,
            "show_follow" : show_follow,
            "user_id" : user_id,
            "page" : posts_paginator
            })
    
    else:
        frequest = request.POST.get("frequest")
        if frequest == "follow":
            follower_list = requested_user.follower.split(",")
            follower_list.append(str(request.user.id))
            requested_user.follower = ','.join(follower_list)

            following_list = logged_user.following.split(",")
            following_list.append(str(user_id))
            logged_user.following = ','.join(following_list)
        else:
            follower_list = requested_user.follower.split(",")
            if str(request.user.id) in follower_list:
                follower_list.remove(str(request.user.id))
            requested_user.follower = ','.join(follower_list)

            following_list = logged_user.following.split(",")
            if str(user_id) in following_list:
                following_list.remove(str(user_id))
            logged_user.following = ','.join(following_list)


        requested_user.save()
        logged_user.save()
        return HttpResponseRedirect(reverse("userpage", kwargs={"user_id" : user_id}))
    
@login_required
def followingfeed(request):
    logged_user = User.objects.get(id= request.user.id)
    following_list = logged_user.following.split(",")
    if not following_list:
        following_list = ['1']
    all_feed = Post.objects.filter(user=following_list[0]).order_by('-creation_date')
    if "" in following_list:
        following_list.remove("")
    for i in following_list:
        all_feed = list(chain(all_feed, Post.objects.filter(user=int(i)).order_by('-creation_date')))

    paginator = Paginator(all_feed, MAX_POSTS)
    page = request.GET.get('page')
    posts_paginator = paginator.get_page(page)

    return render(request, "network/following.html",{
        "posts" : all_feed,
        "page" : posts_paginator
    })


@csrf_exempt
@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    new_content = json.loads(request.body)['new_content']
    if post.content != new_content:
        post.edited = True
        post.content = new_content
        post.save()
    return JsonResponse({'status': 'ok', 'content': post.content})


@csrf_exempt
@login_required
def like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        likers = post.likers.split(",")
        print(likers)
        if str(request.user.id) in likers:
            post.likes = post.likes - 1
            likers.remove(str(request.user.id))
            post.likers = ','.join(likers)
            animation = 'unlike'
        else:
            post.likes = post.likes + 1
            likers.append(str(request.user.id))
            post.likers = ','.join(likers)
            animation = 'like'
        post.save()
        return JsonResponse({'status': 'ok', 'likes' : post.likes, 'animation' : animation})
    except:
        return error(request,"Not Possible :(")
