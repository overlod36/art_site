from django.urls import path
from . import views


urlpatterns = [
    path('course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:id>', views.get_course, name='course-view')
]