from django.urls import path

from user_panel_module import views

urlpatterns = [
    path('', views.MyProfileView.as_view(), name='my_profile_page'),
    path('edit/', views.EditProfileView.as_view(), name='edit_profile_page'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),
    path('comments-list/about-doctor/', views.AboutDrCommentsView.as_view(), name='about_dr_comments_list'),
    path('comments-list/blogha/', views.BlogsCommentsView.as_view(), name='blogs_comments_list'),
    path('blogs-list/', views.BlogsListPanelView.as_view(), name='blogs_list_panel_page'),
    path('create-blog/', views.CreateNewBlogView.as_view(), name='create_new_blog_page'),
    path('edit-blog/<slug:slug>', views.EditBlogView.as_view(), name='edit_blog_page'),
    path('about-doctor-edit/<int:pk>/', views.EditAboutDr.as_view(), name='about_doctor_edit'),
    path('working_hours/', views.CreateWorkingHoursView.as_view(), name='create_working_hours'),
    path('blog-category/', views.BlogCategoryView.as_view(), name='create_blog_category'),
]