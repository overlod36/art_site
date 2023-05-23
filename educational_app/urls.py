from django.urls import path
from . import views


urlpatterns = [
    path('course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:id>', views.get_course, name='course-view'),
    path('student-gradebook/<int:student_id>/', views.get_student_gradebook, name='student-gradebook'),
    path('gradebook/<int:teacher_id>/global', views.get_global_gradebook, name='global_gradebook'),
    # path('course/<int:id>/gradebook/<int:group_num>', views.get_course_gradebook, name='course-gradebook'),
    path('lecture/<int:id>', views.get_lecture, name='download-lec'),
    path('course/lecture/delete/<pk>', views.LectureDeleteView.as_view(), name='lecture-delete'),
    path('course/<int:id>/lecture/upload', views.LectureCreateView.as_view(), name='lecture-upload'),
    path('course/<int:course_id>/test/<int:test_id>', views.get_test, name='test'),
    path('course/<int:id>/test/create', views.TestCreateView.as_view(), name='test-create'),
    path('course/<int:course_id>/test/<int:test_id>/update', views.update_test, name='test-update'),
    path('course/<int:course_id>/test/<int:test_id>/render', views.render_test, name='test-render'),
    path('course/<int:course_id>/test/<int:test_id>/attempts', views.get_test_attempts, name='test-attempts'),
    path('course/<int:course_id>/test/<int:test_id>/attempt/<int:attempt_id>', views.get_test_attempt, name='test-attempt'),
    path('course/<int:course_id>/test/<int:test_id>/attempt/check/<int:attempt_id>', views.check_test_attempt, name='test-attempt-check'),
    path('course/<int:course_id>/test/<int:test_id>/question/delete/<pk>', views.delete_question, name='question-delete'),
    path('course/<int:course_id>/task/create', views.TaskCreateView.as_view(), name='task-create'),
    path('course/<int:course_id>/task/<pk>/publish', views.task_publish, name='task-publish'),
    path('course/<int:course_id>/task/<pk>/close', views.task_close, name='task-close'),
    path('course/<int:course_id>/task/<pk>/update', views.TaskUpdateView.as_view(), name='task-update'),
    path('course/<int:course_id>/task/<pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    path('course/<int:course_id>/task/<int:task_id>/attempts', views.get_task_attempts, name='task-attempts'),
    path('course/<int:course_id>/task/<int:task_id>/attempts/<int:attempt_id>', views.get_task_attempt, name='task-attempt'),
    path('course/<int:course_id>/task/<int:task_id>/attempts/<int:attempt_id>/check', views.check_task_attempt, name='task-attempt-check'),
    path('course/<int:course_id>/task/<int:task_id>/attempts/<int:attempt_id>/file/<int:file_id>', views.get_task_attempt_file, name='task-attempt-file'),
    path('course/<int:course_id>/task/<int:task_id>/solution', views.send_task_attempt, name='task-attempt-create'),
]