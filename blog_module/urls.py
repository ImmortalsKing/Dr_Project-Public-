from django.urls import path

from blog_module import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list_page'),
    path('services/', views.BlogListView.as_view(), name='blog_list_page_by_services'),
    path('womens-issues/', views.BlogListView.as_view(), name='blog_list_page_by_issues'),
    path('<slug:slug>/', views.BlogDetailsView.as_view(), name='blog_details_page'),
]