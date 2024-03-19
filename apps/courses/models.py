from django.db import models
from django.urls import reverse


# Create your models here.

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    index_num = models.IntegerField()
    media = models.FileField(upload_to='media/', blank=True, null=True)
    cover = models.ImageField(upload_to='media/covers/', blank=False, default='https://dummyimage.com/400x225')
    total_time = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail', args=[str(self.course.id), str(self.id)])

    def get_media_url(self):
        return self.media.url


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='media/covers/', blank=True, null=True)
    course_path = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course-detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name
