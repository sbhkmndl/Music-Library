from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from mutagen.mp3 import MP3


User = settings.AUTH_USER_MODEL


def upload_image_location(instance, filename):
    return "%s/img/%s" % (instance.id, filename)


def upload_music_location(instance, filename):
    return "%s/music/%s" % (instance.id, filename)


class Album(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200, null=True, blank=True)
    album_type = models.CharField(max_length=50)
    share = models.BooleanField(default=True)
    album_cover = models.ImageField(upload_to=upload_image_location,
                                    null=True, blank=True,
                                    height_field='height_field',
                                    width_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_albums')
    create_time = models.DateTimeField(auto_now_add=True)
    last_uploaded = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_share(self):
        return self.share


class Playlist(models.Model):
    name = models.CharField(max_length=150)
    playlist_type = models.CharField(max_length=50)
    share = models.BooleanField(default=True)
    playlist_cover = models.ImageField(upload_to=upload_image_location,
                                       null=True, blank=True,
                                       height_field='height_field',
                                       width_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_playlists')
    create_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_share(self):
        return self.share


class Artist(models.Model):
    name = models.CharField(max_length=150, unique=True)
    about = models.CharField(max_length=300, blank=True, null=True)
    artist_image = models.ImageField(upload_to=upload_image_location,
                                     null=True, blank=True,
                                     height_field='height_field',
                                     width_field='height_field'
                                     )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return self.name


def pre_save_artist_lowercase(sender, instance, *args, **kargs):
    instance.name = instance.name.lower()


pre_save.connect(pre_save_artist_lowercase, sender=Artist)


class Music(models.Model):
    name = models.CharField(max_length=150)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='album_musics')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    music_type = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    share = models.BooleanField(default=True)
    file = models.FileField(upload_to=upload_music_location,
                            null=False, blank=False)
    duration_min = models.CharField(max_length=10)
    duration_sec = models.CharField(max_length=3)
    music_cover = models.ImageField(upload_to=upload_image_location,
                                    null=True, blank=True,
                                    height_field='height_field',
                                    width_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_musics')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_share(self):
        return self.share


def music_duration_save(sender, instance, *args, **kargs):
    audio = MP3(instance.file)
    length = audio.info.length
    instance.duration_min = int(length // 60)
    sec = int(length % 60)
    if sec<10:
        sec = '0'+str(sec)
    instance.duration_sec = sec


pre_save.connect(music_duration_save, sender=Music)


def music_add_album_update(sender, instance, created, *args, **kargs):
    if created:
        try:
            if instance.album:
                album_obj = Album.objects.filter(id=instance.album.id).first()
                album_obj.last_uploaded = timezone.now
                album_obj.save()
        except:
            pass


post_save.connect(music_add_album_update, sender=Music)


class PlaylistMusic(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_set')
    song_id = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='playlist_musics')

    def __str__(self):
        return str(self.id)
