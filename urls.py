from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Main page
    path('register/', views.index, name='index'),
    path('login/', views.login, name='login'),
     path('block_user/<int:reg_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:reg_id>/', views.unblock_user, name='unblock_user'),
    path('profile/', views.profile, name='profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('education/', views.education, name='education'),
    path('family/', views.family, name='family'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('adminmain/', views.adminmain_view, name='adminmain_view'),
    path('delete_user/<int:reg_id>/', views.delete_user, name='delete_user'),
    path('review-users/', views.review_users, name='review_users'),
    path('add-plan/', views.add_plan, name='add_plan'),
    path('view-plans/', views.view_plans, name='view_plans'),
    path('plans/edit/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('plans/delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('create-notification/', views.create_notification, name='create_notification'),
    path('delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('logout/', views.logout, name='logout'),

]
