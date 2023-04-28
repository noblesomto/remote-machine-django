from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('serviceman/login', views.login, name='login'),
    path('serviceman/dashboard', views.dashboard, name='dashboard'),
    path('serviceman/request-assistance/<str:machine_id>', views.request_assistance, name='request_assistance'),
    path('serviceman/run-daignostics/<str:id>', views.run_daignostics, name='run_daignostics'),
    path('serviceman/start-monitoring/<str:id>', views.start_monitoring, name='start_monitoring'),
    path('serviceman/software-updates/<str:id>', views.software_updates, name='software_updates'),
    path('serviceman/requests', views.requests, name='requests'),
    path('serviceman/solved-requests', views.solved_requests, name='solved_requests'),
    path('serviceman/request-details/<str:id>', views.request_details, name='request_details'),
    path('serviceman/contact', views.contact, name='contact'),
    path('serviceman/monitor-machine/<str:machine_id>', views.monitor_machine, name='monitor_machine'),
    path('serviceman/notification', views.notification, name='notification'),
    path('serviceman/get-ajax-notification', views.get_ajax_notification, name='get_ajax_notification'),
    path('serviceman/chat-expert/<str:expert_id>/<str:machine_id>', views.chat_expert, name='chat_expert'),
    path('serviceman/chat/<str:machine_id>/<str:req_id>', views.chat, name='chat'),
    path('serviceman/ajax-chat/<str:machine_id>/<str:req_id>', views.ajax_chat, name='ajax_chat'),
    path('serviceman/ajax-post-chat/<str:machine_id>/<str:req_id>', views.ajax_post_chat, name='ajax_post_chat'),
    path('serviceman/chat-worker/<str:machine_id>/<str:req_id>', views.chat_worker, name='chat_worker'),
    path('serviceman/ajax-chat-worker/<str:machine_id>/<str:req_id>', views.ajax_chat_worker, name='ajax_chat_worker'),
    path('serviceman/ajax-post-chat-worker/<str:machine_id>/<str:req_id>', views.ajax_post_chat_worker, name='ajax_post_chat_worker'),
    path('serviceman/video-call/<str:id>', views.video_call, name='video_call'),
    path('serviceman/video-call-2/<str:id>', views.video_call_2, name='video_call_2'),
    path('serviceman/search', views.search, name='search'),

]
