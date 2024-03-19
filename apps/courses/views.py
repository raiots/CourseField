from django.shortcuts import render
from django.views import View
from apps.courses.models import Course, Lesson


# Create your views here.
class IndexView(View):
    def get(self, request):
        course_list = Course.objects.all()
        context = {'course_list': course_list}

        from .auto_importer import get_course_media
        get_course_media()
        return render(request, 'courses/index.html', context)


class CourseDetailView(View):
    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        context = {'lesson_list': course.lesson_set.all(), 'course': course}
        return render(request, 'courses/course_detail.html', context)


class LessonDetailView(View):
    def get(self, request, pk, lesson_pk):
        lesson = Lesson.objects.get(pk=lesson_pk)
        context = {'lesson': lesson}
        return render(request, 'courses/lesson_detail.html', context)