from django.urls import path

from gallery_module import views

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery_page'),
]