from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('page/admin', views.admin, name='admin'),
    path('page/upload_image', views.upload_image, name="upload_image"),


]