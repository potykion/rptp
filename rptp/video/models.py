from django.db import models


class Video(models.Model):
    """
    Represents video with title, preview image, url and other vk info (duration, views).
    """
    title = models.CharField(max_length=500)

    preview = models.URLField()
    url = models.URLField()
    mobile_url = models.URLField()

    duration = models.IntegerField()
    views = models.IntegerField()
