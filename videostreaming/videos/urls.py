# videos/urls.py
from django.urls import path
from .views import VideoViewSet, video_list, user_login, user_logout, user_register, video_create, video_edit, video_delete, video_stream, VideoListView, VideoDetailView, VideoStreamView


urlpatterns = [
    path('videos/', VideoViewSet.as_view({'get': 'list', 'post': 'create'}), name='video-list'),
    path('videos/<int:pk>/', VideoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='video-detail'),
    path('video-list/', video_list, name='video-list-view'),
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('register/', user_register, name='user-register'),
    path('create/', video_create, name='video-create'),
    path('edit/<int:pk>/', video_edit, name='video-edit'),
    path('delete/<int:pk>/', video_delete, name='video-delete'),
    path('video/stream/<int:video_id>/', video_stream, name='video-stream'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos/stream/<int:pk>/', VideoStreamView.as_view(), name='video-stream'),

]
