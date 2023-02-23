from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('serviceman/login', views.login, name='login'),
    path('serviceman/dashboard', views.dashboard, name='dashboard'),
    path('serviceman/run-daignostics/<str:id>', views.run_daignostics, name='run_daignostics'),
    path('serviceman/start-monitoring/<str:id>', views.start_monitoring, name='start_monitoring'),
    path('serviceman/software-updates/<str:id>', views.software_updates, name='software_updates'),
    path('serviceman/requests', views.requests, name='requests'),
    path('serviceman/solved-requests', views.solved_requests, name='solved_requests'),
    path('serviceman/request-details/<str:id>', views.request_details, name='request_details'),
    path('serviceman/contact', views.contact, name='contact'),
    path('serviceman/notification', views.notification, name='notification'),
    path('serviceman/chat-expert/<str:expert_id>/<str:machine_id>', views.chat_expert, name='chat_expert'),
    path('serviceman/chat/<str:machine_id>/<str:req_id>', views.chat, name='chat'),
    path('serviceman/video-call/<str:id>', views.video_call, name='video_call'),
    path('serviceman/search', views.search, name='search'),

]
