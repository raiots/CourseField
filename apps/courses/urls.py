from django.conf.urls.static import static
from django.urls import path, include

from CourseField import settings
from . import views


app_name = 'courses'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
