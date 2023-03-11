from django.urls import path
from . import views


urlpatterns = [
    path('announces/', views.announces, name='announces'),
    path('ann/new/', views.CourseAnnounceCreateView.as_view(), name='ann-create'),
]
