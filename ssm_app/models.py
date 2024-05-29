from django.contrib.auth.models import User
from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def songs(self):
        return Song.objects.filter(playlists__in=[self, ])

    def __str__(self):
        return f'{self.name} {self.user}'


class Album(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'First name: {self.first_name}, Last name: {self.last_name}'


class Song(models.Model):
    class State(models.IntegerChoices):
        LIKED = 1

    title = models.CharField(max_length=128)
    artists = models.ManyToManyField(Artist)
    playlists = models.ManyToManyField(Playlist, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.DO_NOTHING, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    description = models.TextField()
    published = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=State.choices)
    file = models.FileField(upload_to="static/media/")
    sample = models.FileField(upload_to="static/sample/")

    def __str__(self):
        return f'Title: {self.title}, Author: {self.artists.first()}'


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_playlists = models.IntegerField()
    max_logins = models.IntegerField()  # Maximum logins automatically
    stripe_subscription_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    payed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)
