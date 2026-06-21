
# --------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=250) #  is requred                #null=True, blank=True
    body=models.TextField()#  is requred #null=True, blank=True
    create_at=models.DateTimeField(default=datetime.now) #(default=datetime.now
    update_at=models.DateTimeField(auto_now=True) 
    likes=models.IntegerField(default=0)
    comment=models.IntegerField(default=0)

     def __str__(self):
        return self.user.username









   


# -----------------------------------------------
class Movie(models.Model):
    movie =models.CharField(max_length=50)
    hall=models.CharField(max_length=20)#choices=h
    date=models.DateField(null=True, blank=True)
    def __str__(self):
        return self.movie
class Guest(models.Model):
    name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)
    def __str__(self):
        return self.name
class Reservation(models.Model):
    user=models.ForeignKey(Guest,related_name="reservation",on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,related_name="reservation",on_delete=models.CASCADE)
# -----------------------------------------------