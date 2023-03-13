import os
import datetime
import time

from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    """Generate upload path for ImageField"""
    filename, ext = os.path.splitext(filename)
    filename = int(time.time())
    return f'{instance.__class__.__name__}/{datetime.datetime.today().strftime("%Y/%m")}/image_{filename}{ext}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    body = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.body[:50]

    def get_replies(self):
        return Comment.objects.filter(parent=self)

    class Meta:
        ordering = ['-created_time']
