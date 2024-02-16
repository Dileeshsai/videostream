# Generated by Django 3.2.24 on 2024-02-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20240216_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_path',
        ),
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(blank=True, default='default_video.mp4', null=True, upload_to='videos/'),
        ),
    ]
