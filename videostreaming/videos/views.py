import cv2
import threading
from django.db import connection
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators import gzip
from rest_framework import viewsets
from .serializers import VideoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import VideoUploadForm


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

def video_list(request):
    videos = Video.objects.all()
    for video in videos:
        video.start_video_stream()   
    return render(request, 'videos/video_list.html', {'videos': videos})
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user-login')
    else:
        form = UserCreationForm()
    return render(request, 'videos/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('video-list-view')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'videos/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('video-list-view')

def video_create(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('video-list-view')
    else:
        form = VideoUploadForm()
    return render(request, 'videos/video_create.html', {'form': form})

def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video-list-view')
    else:
        form = VideoUploadForm(instance=video)
    return render(request, 'videos/video_edit.html', {'form': form, 'video': video})

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('video-list-view')
    return render(request, 'videos/video_delete.html', {'video': video})

class VideoCamera:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.frame = None
        self.thread = threading.Thread(target=self._update, args=())
        self.thread.daemon = True
        self.thread.start()

    def _update(self):
        while True:
            if self.video.isOpened():
                (grabbed, frame) = self.video.read()
                if not grabbed:
                    break
                self.frame = frame

    def get_frame(self):
        return self.frame

def video_stream(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    
    # Define a generator function to generate video frames
    def generate_frames():
        cap = cv2.VideoCapture(video.video_path)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # You may need to encode the frame if required
            _, buffer = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')

        cap.release()

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
class VideoListView(View):
    def get(self, request):
        videos = Video.objects.all()
        return render(request, 'videos/video_list.html', {'videos': videos})

class VideoDetailView(View):
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        return render(request, 'videos/video_detail.html', {'video': video})

class VideoStreamView(View):
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_path = video.video_path

        response = FileResponse(open(video_path, 'rb'))
        connection.close()  # Close the database connection after serving the file
        return response
class VideoUploadView(View):
    template_name = 'videos/video_upload.html'

    def get(self, request):
        form = VideoUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('video-list')

        return render(request, self.template_name, {'form': form})
