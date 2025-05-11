from django.urls import path

from faq_module import views

urlpatterns = [
    path('', views.FaqView.as_view(), name='faq_page'),
]