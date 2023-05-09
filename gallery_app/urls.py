from django.urls import path
from . import views

urlpatterns = [
    path('st-gallery/<int:id>/', views.get_student_gallery, name='student-gallery'),
    path('st-gallery/<int:id>/upload', views.StudentPictureCreateView.as_view(), name='st-pic-load'),
    path('st-galleries/', views.StudentGalleryListView.as_view(), name='student-galleries'),
    path('st-picture/<pk>/delete', views.StudentPictureDeleteView.as_view(), name='st-pic-del'),
    path('st-picture/<pk>/update', views.StudentPictureUpdateView.as_view(), name='st-pic-upd'),
    path('public-gallery/<int:id>', views.get_public_gallery, name='public-gallery'),
    path('public-gallery/new', views.create_public_gallery, name='public-gallery-new'),
    path('public-gallery/<int:id>/load', views.load_public_picture, name='pub-pic-load'),
    path('public-gallery/<pk>/delete', views.PublicGalleryDeleteView.as_view(), name='public-gallery-del'),
    path('public-gallery/<pk>/update', views.PublicGalleryUpdateView.as_view(), name='public-gallery-upd'),
    path('public-picture/<pk>/delete', views.PublicPictureDeleteView.as_view(), name='public-picture-del'),
    path('public-picture/<pk>/update', views.PublicPictureUpdateView.as_view(), name='public-picture-upd')
]