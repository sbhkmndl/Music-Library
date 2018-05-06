from django.conf.urls import url
from django.urls import path, re_path

from .views import (MusicHomeView,
                    MusicPlayView,
                    AlbumPlayView,
                    PlaylistPlayView,
                    MusicSearchView,
                    MusicShowAllView,
                    AlbumShowAllView,
                    PlaylistShowAllView,
                    ArtistView,
                    ArtistMusicView,
                    ArtistAlbumView,
                    AlbumView,
                    UploaderView,
                    UploaderMusicView,
                    UploaderAlbumView,
                    UploaderPlaylistView,
                    AddPlaylistMusic,
                    PlaylistView)

urlpatterns = [
    path('', MusicHomeView.as_view(), name='music_home'),
    re_path(r'^music/play/(?P<id>\d+)/$', MusicPlayView.as_view(), name='music_play'),
    re_path(r'^album/play/(?P<id>\d+)/$', AlbumPlayView.as_view(), name='album_play'),
    re_path(r'^playlist/play/(?P<id>\d+)/$', PlaylistPlayView.as_view(), name='playlist_play'),
    path('search/', MusicSearchView.as_view(), name='music_search'),
    path('search/music', MusicShowAllView.as_view(), name='music_all'),
    path('search/album', AlbumShowAllView.as_view(), name='album_all'),
    path('search/playlist', PlaylistShowAllView.as_view(), name='playlist_all'),
    path('artist/', ArtistView.as_view(), name='artist_view'),
    path('artist/music/', ArtistMusicView.as_view(), name='artist_music_view'),
    path('artist/album/', ArtistAlbumView.as_view(), name='artist_album_view'),
    re_path('^album/(?P<id>\d+)/$', AlbumView.as_view(), name='album_view'),
    re_path('^playlist/(?P<id>\d+)/$', PlaylistView.as_view(), name='playlist_view'),
    path('uploader/', UploaderView.as_view(), name='uploader_view'),
    path('uploader/music/', UploaderMusicView.as_view(), name='uploader_music_view'),
    path('uploader/album/', UploaderAlbumView.as_view(), name='uploader_album_view'),
    path('uploader/playlist/', UploaderPlaylistView.as_view(), name='uploader_playlist_view'),
    re_path(r'^add/playlist/(?P<playlist_id>\d+)/music/(?P<music_id>\d+)/$', AddPlaylistMusic.as_view(), name='playlist_add'),

]
