from re import T
from tkinter import CASCADE
from turtle import title
from urllib import request
from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate



class Title(models.Model):
     name = models.CharField(max_length=200,null=False)
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)
     class Meta:
        ordering = ['name']
     def __str__(self):
          return self.name




class YhForm(models.Model):
     
     per_choise =((5, 5),(10, 10),(15, 15),(20, 20),(25, 25),(30, 30),(35, 35),(40,40),(45, 45),(50, 50),(55, 55),(60, 60),(65, 65),(70,70),(75, 75),(80, 80),(85, 85),(90, 90),(95, 95),(100,100))
     username = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
     title = models.ForeignKey(Title,on_delete=models.CASCADE,blank=False, null=False)
     date = models.DateField(blank=False, null=False)
     percent= models.IntegerField(choices=per_choise,blank=False, null=False)
     comments = models.TextField( default='',blank=True,null=True)
     gl=models.CharField(max_length=100,null=False)
     dm=models.CharField(max_length=200,null=False)
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)
     def __int__(self):
          return self.id 


class UserTitle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.title.name}"




