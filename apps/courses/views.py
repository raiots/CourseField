import json

from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
from django.views import View
from apps.courses.models import Course, Lesson
from apps.users.models import User, PlayHistory


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
        from .auto_importer import add_lesson
        add_lesson(course)
        context = {'lesson_list': course.lesson_set.all(), 'course': course}
        return render(request, 'courses/course_detail.html', context)


class LessonDetailView(View):
    def get(self, request, course_pk, lesson_pk):
        lesson = Lesson.objects.get(pk=lesson_pk)
        play_history = PlayHistory.objects.filter(lesson=lesson, user=request.user).first()
        if play_history:
            play_time = play_history.time
        else:
            play_time = 0
        print(play_time)

        context = {'lesson': lesson, 'play_time': play_time}
        return render(request, 'courses/lesson_detail.html', context)

    def post(self, request, course_pk, lesson_pk):
        # print the post data
        print(json.loads(request.body))
        play_time = json.loads(request.body)['time']

        PlayHistory.objects.update_or_create(
            lesson=Lesson.objects.get(pk=lesson_pk),
            user=User.objects.get(id=request.user.id),
            defaults={'time': play_time}
        )

        return JsonResponse({'status': 'ok'}, status=200)