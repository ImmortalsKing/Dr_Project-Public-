from django.urls import path

from home_module import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    # path('subscribe',views.SubscribeToNewsletter.as_view(),name='subscribe_to_newsletter'),
    path('remove-subscription/<str:email>',views.RemoveFromNewsletter.as_view(),name='remove_subscription'),
]