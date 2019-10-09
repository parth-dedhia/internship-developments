from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, unique=False , on_delete=models.CASCADE,)
    priority = models.IntegerField(default=0)
    task = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

