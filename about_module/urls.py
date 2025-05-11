from django.urls import path

from about_module import views

urlpatterns = [
    path('about-dr/', views.AboutDoctor.as_view(), name='about_dr_page')
]