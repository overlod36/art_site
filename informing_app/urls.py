from django.urls import path
from . import views


urlpatterns = [
    path('announces/', views.announces, name='announces'),
    path('course/<int:pk>/ann/new/', views.OneCourseAnnounceCreateView.as_view(), name='one-ann-create'),
    path('ann/new/', views.CourseAnnounceCreateView.as_view(), name='ann-create'),
    path('ann/delete/<int:id>', views.delete_announce, name='delete-announce'),
    path('news/delete/<int:id>', views.delete_news, name='delete-news'),
    path('news/new/', views.NewsAnnounceCreateView.as_view(), name='news-create')
]
