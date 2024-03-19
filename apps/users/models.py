from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.courses.models import Course, Lesson


# Create your models here.



class User(AbstractUser):
    pass


class PlayHistory(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    time = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
