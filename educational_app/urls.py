from django.urls import path
from . import views


urlpatterns = [
    path('course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:id>', views.get_course, name='course-view'),
    # path('course/<int:id>/gradebook/<int:group_num>', views.get_course_gradebook, name='course-gradebook'),
    path('lecture/<int:id>', views.get_lecture, name='download-lec'),
    path('course/lecture/delete/<pk>', views.LectureDeleteView.as_view(), name='lecture-delete'),
    path('course/<int:id>/lecture/upload', views.LectureCreateView.as_view(), name='lecture-upload'),
    path('course/<int:course_id>/test/<int:test_id>', views.get_test, name='test'),
    path('course/<int:id>/test/create', views.TestCreateView.as_view(), name='test-create'),
    path('course/<int:course_id>/test/<int:test_id>/update', views.update_test, name='test-update'),
    path('course/<int:course_id>/test/<int:test_id>/question/delete/<pk>', views.delete_question, name='question-delete'),
    # path('test/<int:id>', views.get_test, name='test'),
    # path('test-attempt/<int:id>', views.get_test_attempt, name='test-attempt'),
    # path('test/<int:id>/close', views.close_test, name='test-close')
]