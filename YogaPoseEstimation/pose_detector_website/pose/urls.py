from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('uploadpose/', views.upload_pose, name='upload_form'),
    path('search/', views.search, name='search'),
    path('upload_webcam/', views.upload_webcam, name='upload_webcam'),
    path('delete/<slug:slug>/', views.delete_pose, name='delete_pose'),
    path('<slug:slug>/', views.details, name='details'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
