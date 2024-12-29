from django.db import models

# Create your models here.
class YouTubeVideo(models.Model):
    kind = models.CharField(max_length=50)
    etag = models.CharField(max_length=255)
    video_id = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    channel_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_default_url = models.URLField()
    thumbnail_default_width = models.IntegerField()
    thumbnail_default_height = models.IntegerField()
    thumbnail_medium_url = models.URLField()
    thumbnail_medium_width = models.IntegerField()
    thumbnail_medium_height = models.IntegerField()
    thumbnail_high_url = models.URLField()
    thumbnail_high_width = models.IntegerField()
    thumbnail_high_height = models.IntegerField()
    channel_title = models.CharField(max_length=255)
    live_broadcast_content = models.CharField(max_length=50)
    publish_time = models.DateTimeField()
    query=models.CharField(max_length=255,default="test")
    
    def __str__(self):
        return self.title
