from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('expert/login', views.login, name='login'),
    path('expert/dashboard', views.dashboard, name='dashboard'),
    path('expert/give-instruction/<str:machine_id>', views.give_instruction, name='give_instruction'),
    path('expert/monitor-machine/<str:machine_id>', views.monitor_machine, name='monitor_machine'),
    path('expert/monitor-cobot/<str:machine_id>', views.monitor_machine, name='monitor_machine'),
    path('expert/machine-status/<str:machine_id>', views.machine_status, name='machine_status'),
    path('expert/maintenance/<str:machine_id>', views.maintenance, name='maintenance'),
    path('expert/requests', views.requests, name='requests'),
    path('expert/request-details/<str:id>', views.request_details, name='request_details'),
    path('expert/contact', views.contact, name='contact'),
    path('expert/notification', views.notification, name='notification'),
    path('expert/workers/<str:id>', views.workers, name='workers'),
    path('expert/serviceman/<str:id>', views.serviceman, name='serviceman'),
    path('expert/chat/<str:machine_id>/<str:req_id>', views.chat, name='chat'),
    path('expert/serviceman-chat/<str:expert_id>/<str:machine_id>', views.chat_serviceman, name='chat_serviceman'),

]
