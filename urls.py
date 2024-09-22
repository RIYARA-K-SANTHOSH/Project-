from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Main page
    path('register/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('profile1/', views.profile_view, name='profile1'),
    path('block_user/<int:reg_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:reg_id>/', views.unblock_user, name='unblock_user'),
    path('profile/', views.profile, name='profile'),
    path('edit_personal_details/', views.edit_personal_details, name='edit_personal_details'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit-profile/<int:reg_id>/', views.edit_profile, name='edit_profile'),
    path('education/', views.education, name='education'),
    path('edit_education/', views.edit_education, name='edit_education'),
    path('family/', views.family, name='family'),
    path('edit_family/', views.edit_family, name='edit_family'),
    path('profile1/<int:reg_id>/', views.profile_view, name='profile1'),  # Ensure this line exists
    path('upload-images/<int:reg_id>/', views.upload_images, name='upload_images'),
    path('view_all_details/<int:personal_id>/', views.view_all_details, name='view_all_details'),
    path('view_profile/<int:personal_id>/', views.view_profile1, name='view_profile1'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('adminmain/', views.adminmain_view, name='adminmain_view'),
    path('delete_user/<int:reg_id>/', views.delete_user, name='delete_user'),
    path('review-users/', views.review_users, name='review_users'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('create-notification/', views.create_notification, name='create_notification'),
    path('delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('logout/', views.logout, name='logout'),

]
