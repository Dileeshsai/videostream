from django.db import models
import threading

class Video(models.Model):
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="videos/", default='default_video.mp4', null=True, blank=True)
    thread = models.PositiveIntegerField(default=0)
    def start_video_stream(self):
        if not self.thread or not threading.Thread.is_alive(threading.Thread(target=self._video_stream)):
            thread = threading.Thread(target=self._video_stream)
            thread.start()
            self.thread = thread.ident
            self.save()

    def _video_stream(self):
        # Implement video streaming logic similar to the `video_stream` view
        if not self.thread or not threading.Thread.is_alive(threading.Thread(target=self._video_stream)):
            thread = threading.Thread(target=self._video_stream)
            thread.start()
            self.thread = thread.ident
            self.save()
        pass

    def __str__(self):
        return self.name
