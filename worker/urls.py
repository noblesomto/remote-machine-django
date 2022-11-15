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
    path('worker/request-details/<str:id>', views.request_details, name='request_details'),
    path('worker/contact', views.contact, name='contact'),
    path('worker/notification', views.notification, name='notification'),
    path('worker/experts/<str:id>', views.experts, name='experts'),
    path('worker/serviceman/<str:id>', views.serviceman, name='serviceman'),
    path('worker/chat/<str:id>/<str:req_id>', views.chat, name='chat'),
]
