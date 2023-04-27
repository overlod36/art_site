from django.urls import path
from . import views

urlpatterns = [
    path('st-gallery/<int:id>/', views.get_student_gallery, name='student-gallery'),
    path('st-gallery/<int:id>/upload', views.StudentPictureCreateView.as_view(), name='pic-load'),
    path('st-galleries/', views.StudentGalleryListView.as_view(), name='student-galleries')
]