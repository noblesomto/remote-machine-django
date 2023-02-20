from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('expert/login', views.login, name='login'),
    path('expert/dashboard', views.dashboard, name='dashboard'),
    path('expert/give-instruction/<str:machine_id>', views.give_instruction, name='give_instruction'),
    path('expert/monitor-machine/<str:machine_id>', views.monitor_machine, name='monitor_machine'),
    path('expert/monitor-cobot/<str:machine_id>', views.monitor_cobot, name='monitor_cobot'),
    path('expert/machine-status/<str:machine_id>', views.machine_status, name='machine_status'),
    path('expert/maintenance/<str:machine_id>', views.maintenance, name='maintenance'),
    path('expert/requests', views.requests, name='requests'),
    path('expert/solved-requests', views.solved_requests, name='solved_requests'),
    path('expert/request-details/<str:id>', views.request_details, name='request_details'),
    path('expert/contact', views.contact, name='contact'),
    path('expert/notification', views.notification, name='notification'),
    path('expert/workers/<str:id>', views.workers, name='workers'),
    path('expert/serviceman/<str:id>', views.serviceman, name='serviceman'),
    path('expert/chat-2/<str:machine_id>/<str:req_id>', views.chat_2, name='chat_2'),
    path('expert/video-call/<str:id>', views.video_call, name='video_call'),
    path('expert/request-status/<str:id>', views.expert_request_status, name='expert_request_status'),
    path('expert/serviceman-chat/<str:machine_id>/<str:req_id>', views.chat_serviceman, name='chat_serviceman'),
    path('expert/define-program/<str:id>', views.define_program, name='define_program'),
    path('expert/simulate-program/<str:machine_id>', views.simulate_program, name='simulate_program'),
    path('expert/send-program/<str:machine_id>', views.send_program, name='send_program'),
    path('expert/activate-webcam/<str:machine_id>', views.activate_webcam, name='activate_webcam'),
    path('expert/service-reminder/<str:id>', views.service_reminder, name='service_reminder'),

]
