from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('worker/login', views.login, name='login'),
    path('worker/dashboard', views.dashboard, name='dashboard'),
    path('worker/assistance/<str:machine_id>', views.assistance, name='assistance'),
    path('worker/failure/<str:machine_id>', views.failure, name='failure'),
    path('worker/requests', views.requests, name='requests'),
    path('worker/solved-requests', views.solved_requests, name='solved_requests'),
    path('worker/request-details/<str:id>', views.request_details, name='request_details'),
    path('worker/contact', views.contact, name='contact'),
    path('worker/notification', views.notification, name='notification'),
    path('worker/notification-details/<str:id>', views.notification_details, name='notification_details'),
    path('worker/experts/<str:id>', views.experts, name='experts'),
    path('worker/monitor-machine/<str:machine_id>', views.monitor_machine, name='monitor_machine'),
    path('worker/connect-smartglass/<str:id>', views.connect_smartglass, name='connect_smartglass'),
    path('worker/connecting-smartglass/<str:id>', views.connecting_smartglass, name='connecting_smartglass'),
    path('worker/serviceman/<str:id>', views.serviceman, name='serviceman'),
    path('worker/chat/<str:expert_id>/<str:req_id>', views.chat, name='chat'),
    path('worker/request-status/<str:id>', views.request_status, name='request_status'),
    path('worker/video-call/<str:id>', views.video_call, name='video_call'),
    path('worker/service-reminder/<str:id>', views.service_reminder, name='service_reminder'),
    path('worker/machine-alarm/<str:id>', views.machine_alarm, name='machine_alarm'),
]
