from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_posts')
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f"{self.pk} by user {self.user}, time: {self.date_time}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_profile', null = True)
    no_followers = models.IntegerField(default = 0)

    def __str__(self):
        return f"ID: {self.pk}, user: {self.user}"


class Following(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')
    user_follows = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_follows')

    def __str__(self):
        return f"{self.user} follows {self.user_follows}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'liked_post')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_liked')

    def __str__(self):
        return f"{self.user} likes {self.post}"
