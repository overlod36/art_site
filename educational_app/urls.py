from django.urls import path
from . import views


urlpatterns = [
    path('course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:id>', views.get_course, name='course-view'),
    path('lectures/<int:id>', views.get_lecture, name='download-lec'),
    path('course/<int:id>/upload/lecture', views.LectureCreateView.as_view(), name='lecture-upload'),
    path('test/<int:id>', views.get_test, name='test')
]