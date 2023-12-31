
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newposter", views.newposter, name="newposter"),
    path("newpost", views.newpost, name="newpost"),
    path("user/<str:username>", views.userpage, name="userpage"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("following", views.followingfeed, name="followingfeed"),
    path("like/<int:post_id>", views.like, name="like"),
    path("post/<int:post_id>", views.postpage, name="postpage"),
    path("edit/profile/<str:username>", views.editprofile, name="editprofile")
]
