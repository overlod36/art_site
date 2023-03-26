from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('student/new', views.StudentCreateView.as_view(), name='student-create'),
    path('teacher/new', views.TeacherCreateView.as_view(), name='teacher-create'),
    path('administrator/new', views.AdminCreateView.as_view(), name='admin-create'),
    path('group/new', views.StudyGroupCreateView.as_view(), name='group-create'),
    path('students/', views.StudentsListView.as_view(), name='students'),
    path('student/delete/<pk>/', views.UserDeleteView.as_view(), name='delete-student'),
    path('student/update/<pk>/', views.StudentUpdateView.as_view(), name='update-student'),
    path('teacher/update/<pk>/', views.TeacherUpdateView.as_view(), name='update-teacher'),
    path('admins/update/<pk>/', views.AdminUpdateView.as_view(), name='update-admin'),
    path('teachers/', views.TeachersListView.as_view(), name='teachers'),
    path('admins/', views.AdminsListView.as_view(), name='admins'),
    path('teacher/delete/<pk>/', views.UserDeleteView.as_view(), name='delete-teacher'),
    path('admins/delete/<pk>/', views.UserDeleteView.as_view(), name='delete-admin'),
    path('users/update/password/<pk>', views.PasswordUpdateView.as_view(), name='update-pass'),
    path('users/update/login/<pk>', views.LoginUpdateView.as_view(), name='update-log')
    
]
