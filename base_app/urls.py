from django.urls import path, include
from . import views, server_methods

urlpatterns = [
	path('', views.index, name='main'),
    path('server-time/', server_methods.get_time, name='time'),
    path('', include('users.urls')),
]