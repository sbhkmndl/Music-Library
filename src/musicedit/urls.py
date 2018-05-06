from django.conf.urls import url
from django.urls import path, re_path
from .views import (UserDetailsView,
                    MusicEditView,
                    AlbumEditView,
                    PlaylistEditView,
                    AlbumMusicEditView,
                    PlaylistMusicEditView,
                    MusicDeleteView,
                    AlbumDeleteView,
                    PlaylistDeleteView,
                    PlaylistMusicDeleteView)
from musiccreate.views import MusicUploadView

urlpatterns = [
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('music/', MusicEditView.as_view(), name='music_edit'),
    path('album/', AlbumEditView.as_view(), name='album_edit'),
    path('playlist/', PlaylistEditView.as_view(), name='playlist_edit'),
    re_path(r'^album/(?P<id>\d+)/$', AlbumMusicEditView.as_view(), name='album_music_edit'),
    re_path(r'^playlist/(?P<id>\d+)/$', PlaylistMusicEditView.as_view(), name='playlist_music_edit'),
    re_path(r'^music/(?P<pk>\d+)/delete/$', MusicDeleteView.as_view(), name='music_delete'),
    re_path(r'^album/(?P<pk>\d+)/delete/$', AlbumDeleteView.as_view(), name='album_delete'),
    re_path(r'^playlist/(?P<pk>\d+)/delete/$', PlaylistDeleteView.as_view(), name='playlist_delete'),
    re_path(r'^album/(?P<album_id>\d+)/uploadMusic/$', MusicUploadView.as_view(), name='album_music_upload'),
    path('music/uploadMusic/', MusicUploadView.as_view(), name='edit_music_upload'),
    re_path(r'^playlistmusic/(?P<pk>\d+)/delete/$', PlaylistMusicDeleteView.as_view(), name='playlist_music_delete')

]
