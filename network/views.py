from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.shortcuts import redirect


from .models import User, Post


def error(request, message):
    return render(request, "network/error.html", {
        "message" : message
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html",{
       "posts" : posts,
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
                text = "Just tryin man"
            thisPost = Post(user=request.user, content=text)
            thisPost.save()
        else:
            return error(request, "No Hacking in my site baby")
    else:
      return error(request, "Not This Way Baby")
    
def newpost(request):
    return render(request, "network/newpost.html")

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
        print(logged_following_list)
        if str(user_id) in  logged_following_list:
            is_following = True
        else:
            is_following = False
        return render(request, "network/userpage.html",{
            "username" : requested_user.username,
            "posts" : posts,
            "followers" : len(requested_user.follower.split(",")),
            "following" : len(requested_user.following.split(",")),
            "is_following" : is_following,
            "show_follow" : show_follow,
            "user_id" : user_id
            })
    
    else:
        frequest = request.POST.get("frequest")
        print(frequest)
        if frequest == "follow":
            follower_list = requested_user.follower.split(",")
            print(f"requested_user follower list : {follower_list}")
            follower_list.append(str(request.user.id))
            requested_user.follower = ','.join(follower_list)

            following_list = logged_user.following.split(",")
            print(f"logged_user following list : {following_list}")
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
    

def followingfeed(request):
    pass
