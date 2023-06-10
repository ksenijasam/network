from django.contrib import admin
from .models import User, Post, UserProfile, Following, Like

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Following)
admin.site.register(Like)
