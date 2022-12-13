from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/dashboard', views.dashboard, name='dashboard'),
    path('users/new-user', views.new_user, name='new_user'),
    path('users/all-users', views.all_users, name='all_users'),
    path('users/edit-user/<str:id>', views.edit_user, name='edit_user'),
    path('users/user-status/<str:id>/<str:status>', views.user_status, name='user_status'),
    path('users/delete-user/<str:id>', views.delete_user, name='delete_user'),

    path('users/new-notification', views.new_notification, name='new_notification'),
    path('users/all-notification', views.all_notification, name='all_notification'),
    path('users/notification-status/<str:id>/<str:status>', views.notification_status, name='notification_status'),
    path('users/delete-notification/<str:id>', views.delete_notification, name='delete_notification'),


    path('users/new-machine', views.new_machine, name='new_machine'),
    path('users/all-machine', views.all_machine, name='all_machine'),
    path('users/edit-machine/<str:id>', views.edit_machine, name='edit_machine'),
    path('users/delete-machine/<str:id>', views.delete_machine, name='deletemachiner'),

    path('users/logout', views.logout, name='logout'),
   

]
