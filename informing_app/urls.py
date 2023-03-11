from django.urls import path
from . import views


urlpatterns = [
    path('announces/', views.announces, name='announces')
]
