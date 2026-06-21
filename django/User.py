from django.contrib.auth.models import User

    # "id": 1,
    # "password": "pbkdf2_sha256$1200000$dkvjFEKE9oRCvoTfpimLiL$kxIEbkxEo97pG3fxYhhZEobaj8kcXM4xYta0IoXTO1w=",
    # "last_login": "2026-06-19T20:54:40.487635Z",
    # "is_superuser": true,
    # "username": "youssef",
    # "first_name": "",
    # "last_name": "",
    # "email": "y@g.com",
    # "is_staff": true,
    # "is_active": true,
    # "date_joined": "2026-06-19T20:40:03.454538Z",
    # "groups": [],
    # "user_permissions": []

# --------------------------------
User.objects.filter(username__iexact=value).exists()
User.objects.filter(email__iexact=value).exists()
User.objects.filter(username=value).exists()
# ----
from django.db.models import Q
exists = User.objects.filter(Q(username__iexact=value) | Q(email__iexact=value)).exists()
# ----
User.objects.get_or_create(...)
user = User.objects.create_user(     username="youssef",     email="test@gmail.com",password="123456")
# --------------------------------
# 
# models
from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    
#settings.py
AUTH_USER_MODEL = "post_api.User"
# --------------------------------
# request.user
# request.user.is_staff
# AnonymousUser