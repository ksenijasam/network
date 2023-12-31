
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save_post", views.save_post, name="save_post"),
    path("get_all_posts", views.get_all_posts, name="get_all_posts"),
    path("profile/<int:id>/<str:follow>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("saveEditedPost/<int:id>", views.save_edited_post, name="save_edited_post"),
    path("liked_posts/<str:path>", views.liked_posts, name="liked_posts"),
    path("liked/<int:id>", views.liked, name="liked")
]

