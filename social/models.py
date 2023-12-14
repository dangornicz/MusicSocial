from django.conf import settings
from django.db import models


class SavedEvent(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    event_name = models.TextField(max_length=100, default="none")
    event_venue = models.TextField(max_length=100, default="none")
    event_city = models.TextField(max_length=100, default="none")
    event_state = models.TextField(max_length=100, default="none")
    event_date = models.TextField(max_length=100, default="none")
    event_image = models.TextField(max_length=100, default="none")
    event_url = models.TextField(max_length=100, default="none")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    saved_event = models.ForeignKey(
        SavedEvent,
        on_delete=models.CASCADE,
    )
    comment_field = models.TextField(max_length=200, default="none")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_field


class Followers(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    time_stamp = models.DateTimeField(auto_now_add=True)


class Bio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bio_field = models.TextField(max_length=200, default="none")
    time_stamp = models.DateTimeField(auto_now_add=True)
