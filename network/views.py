from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect,JsonResponse
from itertools import chain
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



from .models import User, Post
LOGIN_URL = '/login'
MAX_POSTS = 10

def error(request, message):
    return render(request, "network/error.html", {
        "message" : message,
        "pagename" : "buffer page"
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def index(request):
    posts = Post.objects.all().order_by('-creation_date')
    #paginations 
    
    return render(request, "network/index.html",{
       "posts" : posts,
       "pagename" : "Home"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        if username.lower() == "arnav":
            return render(request, "network/login.html", {
                "message": "Boss said to not log you in :(",
                "pagename" : "Login"
            })
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password.","pagename": "Login"
            })
    else:
        return render(request, "network/login.html",{"pagename" : "Login"})


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
                "message": "Passwords must match.",
                "pagename" : "Register"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username.lower(), email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken.",
                "pagename" : "Register"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {"pagename" : "Register"})

@login_required(login_url=LOGIN_URL )   
def newposter(request):
    if request.method == "POST":
        text = request.POST.get("content")
        if not text:
            return error(request, "Must provide a content")
        thisPost = Post(user=request.user, content=text)
        thisPost.save()
        return error(request, "Posted !! ")
    else:
      return error(request, "Not This Way Baby")
    
def newpost(request):
    return render(request, "network/newpost.html",{"pagename" : "New Post"})

def userpage(request, username ):
    requested_user = User.objects.get(username=username)
    requested_user_id = requested_user.id
    if request.user.is_authenticated:
        logged_user = User.objects.get(id= request.user.id)
        logged_following_list = logged_user.following.split(",")
        if str(requested_user_id) in  logged_following_list:
            is_following = True
        else:
            is_following = False
    else:
        is_following = False

    if request.method  == "GET":
        posts = Post.objects.filter(user=requested_user_id).order_by('-creation_date')
        if request.user.id == requested_user_id:
            show_follow = False
        else:
            show_follow = True
        return render(request, "network/userpage.html",{
            "profile_user" : requested_user,
            "posts" : posts,
            "followers" : len(requested_user.follower.split(",")),
            "following" : len(requested_user.following.split(",")),
            "is_following" : is_following,
            "show_follow" : show_follow,
            "pagename" : requested_user.username,
            "total_posts": len(posts)
            })
    
    else:
        frequest = request.POST.get("frequest")
        if frequest == "follow":
            follower_list = requested_user.follower.split(",")
            follower_list.append(str(request.user.id))
            requested_user.follower = ','.join(follower_list)

            following_list = logged_user.following.split(",")
            following_list.append(str(requested_user_id))
            logged_user.following = ','.join(following_list)
        else:
            follower_list = requested_user.follower.split(",")
            if str(request.user.id) in follower_list:
                follower_list.remove(str(request.user.id))
            requested_user.follower = ','.join(follower_list)

            following_list = logged_user.following.split(",")
            if str(requested_user_id) in following_list:
                following_list.remove(str(requested_user_id))
            logged_user.following = ','.join(following_list)


        requested_user.save()
        logged_user.save()
        return HttpResponseRedirect(reverse("userpage", kwargs={"username" : username}))
    
@login_required(login_url=LOGIN_URL )
def followingfeed(request):
    logged_user = User.objects.get(id= request.user.id)
    following_list = logged_user.following.split(",")
    if "" in following_list:
        following_list.remove("")
    try:
        all_feed = Post.objects.filter(user=following_list[0]).order_by('-creation_date')
        for i in following_list:
            all_feed = list(chain(all_feed, Post.objects.filter(user=int(i)).order_by('-creation_date')))
    except:
        all_feed=[]

    return render(request, "network/following.html",{
        "posts" : all_feed,
        "pagename" : "Following Feed"
    })


@csrf_exempt
@login_required(login_url=LOGIN_URL)
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user.id == post.user.id:
        new_content = json.loads(request.body)['new_content']
        if new_content.replace(" ","") == "":
            pass
        elif post.content != new_content:
            post.edited = True
            post.content = new_content
            post.save()

        return JsonResponse({'status': 'ok', 'content': post.content})
    else:
        return error(request, "Not your post to edit")


@csrf_exempt
@login_required(login_url=LOGIN_URL )
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


def postpage(request,post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "network/postpage.html", {
        "post" : post
    })

def editprofile(request, username):
    if request.method == "GET":
        if request.user.username == username:
            return render(request, "network/editprofile.html",{
                "pagename" : f"Edit Profile : {username}"
            })
        else:
            return error(request, "Denied")
    else: 
        this_user = User.objects.get(username=username)
        password = request.POST['password']
        if this_user.check_password(password):
            new_username = request.POST['username']
            new_email = request.POST['email']
            new_first_name = request.POST['first_name']
            new_last_name = request.POST['last_name']
            new_bio = request.POST['bio']
            if 'pfp' in request.FILES:
                new_pfp = request.FILES['pfp']
                this_user.pfp = new_pfp
            this_user.username = new_username
            this_user.email = new_email
            this_user.first_name = new_first_name
            this_user.last_name = new_last_name
            this_user.bio = new_bio
            print(this_user.first_name)
            this_user.save()
        else:
            return render(request, "network/editprofile.html",{
                "pagename" : f"Edit Profile : {username}",
                "message" : "Incorrect Password"
            })
        return HttpResponseRedirect(reverse("userpage", kwargs={"username" : new_username}))
        
        