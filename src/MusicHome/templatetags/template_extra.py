from django import template
from django.template import Template

from musiccreate.models import Playlist, Album, PlaylistMusic

register = template.Library()


@register.inclusion_tag('home/get_playlist.html')
def get_albums(request):
    playlist_list = ''
    if request.user.is_authenticated:
        playlist_list = Playlist.objects.filter(uploaded_by=request.user)
    print(playlist_list)
    return {'playlist_list': playlist_list}


@register.simple_tag
def name_capitalize(names):
    return " ".join(name.capitalize() for name in names.split(' '))


@register.simple_tag
def no_album_music(album):
    return int(album.album_musics.all().count()) == 0


@register.simple_tag
def no_playlist_music(playlist):
    return int(playlist.playlist_set.all().count()) == 0


@register.simple_tag
def get_delete_playlist_id(playlist_id, music_id):
    return PlaylistMusic.objects.filter(playlist_id_id=playlist_id, song_id_id=music_id).first().id
