from django.conf.urls import url
from django.urls import path, re_path
from .views import UserUpdateView, AlbumCreateView, PlaylistCreateView, MusicUploadView, ArtistCreateView


urlpatterns = [
    path('updateUser/', UserUpdateView.as_view(), name='user_update'),
    path('album/', AlbumCreateView.as_view(), name='create_album'),
    path('playlist/', PlaylistCreateView.as_view(), name='create_playlist'),
    path('music/', MusicUploadView.as_view(), name='upload_music'),
    path('artist/', ArtistCreateView.as_view(), name='artist_add'),
]
