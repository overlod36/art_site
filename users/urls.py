from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('student/new', views.StudentCreateView.as_view(), name='student-create'),
    path('teacher/new', views.TeacherCreateView.as_view(), name='teacher-create'),
    path('administrator/new', views.AdminCreateView.as_view(), name='admin-create')
]
