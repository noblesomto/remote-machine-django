from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('serviceman/login', views.login, name='login'),
    path('serviceman/dashboard', views.dashboard, name='dashboard'),
    path('serviceman/run-maintenance/<str:machine_id>', views.run_maintenance, name='run_maintenance'),
    path('serviceman/requests', views.requests, name='requests'),
    path('serviceman/request-details/<str:id>', views.request_details, name='request_details'),
    path('serviceman/contact', views.contact, name='contact'),
    path('serviceman/notification', views.notification, name='notification'),
    path('serviceman/chat-expert/<str:expert_id>/<str:machine_id>', views.chat_expert, name='chat_expert'),

]
