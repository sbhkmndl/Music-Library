from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, CreateView
from django.views.generic.base import View

from musiccreate.models import Music, Album, Playlist, PlaylistMusic, Artist
from userprofile.models import UserDetail
# Create your views here.


class MusicHomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(MusicHomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('-upload_time')[:5]
            album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('last_uploaded')[:5]
            playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('last_update')[:5]
        else:
            music_obj = Music.objects.filter(Q(share=True)).order_by('upload_time')[:5]
            album_obj = Album.objects.filter(Q(share=True)).order_by('last_uploaded')[:5]
            playlist_obj = Playlist.objects.filter(Q(share=True)).order_by('last_update')[:5]
        if music_obj:
            context['music_obj'] = music_obj
        if album_obj:
            context['album_obj'] = album_obj
        if playlist_obj:
            context['playlist_obj'] = playlist_obj
        return context


class MusicPlayView(DetailView):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            music_id = kwargs.get('id')
            if music_id:
                music_details = Music.objects.filter(id=music_id).first()
                music_img = ''
                music_album = ''
                music_album_link = ''
                if music_details.music_cover:
                    music_img = music_details.music_cover.url
                if music_details.album:
                    music_album = music_details.album.name
                    music_album_link = reverse('album_view', kwargs={'id': music_details.album_id})

                    # music_album_link = '/album/'+str(music_details.album_id)
                artist_link = '/artist/?q='+music_details.artist.name
                data = {
                    'music_url': [music_details.file.url],
                    'music_img': [music_img],
                    'music_name': [music_details.name],
                    'music_artist': [music_details.artist.name],
                    'music_album': [music_album],
                    'artist_link': [artist_link],
                    'music_album_link': [music_album_link],
                    'music_id': [music_details.id]
                }
                return JsonResponse(data)
        return JsonResponse(data)


class AlbumPlayView(DetailView):
    def get(self, request, *args, **kwargs):
        print()
        data = {}
        if request.is_ajax():
            album_id = kwargs.get('id')
            if album_id:
                if request.user.is_authenticated:
                    music_details = Music.objects.filter(Q(album=album_id), Q(share=True) | Q(uploaded_by=self.request.user))
                else:
                    music_details = Music.objects.filter(Q(album=album_id), Q(share=True))
                data = album_playlist_play_data(music_details)
                return JsonResponse(data)
        return JsonResponse(data)


class PlaylistPlayView(DetailView):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            plsylist_id = kwargs.get('id')
            if plsylist_id:
                playlist_music_id = [music.song_id_id for music in PlaylistMusic.objects.filter(playlist_id=plsylist_id)]
                if request.user.is_authenticated:
                    music_details = Music.objects.filter(Q(id__in=playlist_music_id), Q(share=True) | Q(uploaded_by=request.user))
                else:
                    music_details = Music.objects.filter(Q(id__in=playlist_music_id), Q(share=True))
                data = album_playlist_play_data(music_details)
                return JsonResponse(data)
        return JsonResponse(data)


def album_playlist_play_data(music_details):
    music_url = []
    music_img = []
    music_name = []
    music_artist = []
    music_album = []
    artist_link = []
    music_album_link = []
    music_id = []
    for album_music in music_details:
        if album_music.music_cover:
            music_img.append(album_music.music_cover.url)
        else:
            music_img.append('')
        if album_music.album:
            music_album.append(album_music.album.name)
            music_album_link.append(reverse('album_view', kwargs={'id': album_music.album_id}))
        else:
            music_album.append('')
            music_album_link.append('')
        music_id.append(album_music.id)
        music_url.append(album_music.file.url)
        music_name.append(album_music.name)
        music_artist.append(album_music.artist.name)
        artist_link.append('/artist/?q=' + album_music.artist.name)

    data = {
        'music_url': music_url,
        'music_img': music_img,
        'music_name': music_name,
        'music_artist': music_artist,
        'music_album': music_album,
        'artist_link': artist_link,
        'music_album_link': music_album_link,
        'music_id': music_id,
    }

    return data


class MusicSearchView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        context = super(MusicSearchView, self).get_context_data(**kwargs)
        category = self.request.GET.get('catagory')
        music_obj = ''
        album_obj = ''
        playlist_obj = ''
        if not category:
            if self.request.user.is_authenticated:
                music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                 Q(name__icontains=query) | Q(artist__name__icontains=query) |
                                                 Q(language__icontains=query), Q(music_type__icontains=query)
                                                 ).order_by('upload_time')[:5]
                album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                 Q(name__icontains=query) | Q(album_type__icontains=query) |
                                                 Q(description__icontains=query)
                                                 ).order_by('last_uploaded')[:5]
                playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                       Q(name__icontains=query) | Q(playlist_type__icontains=query)
                                                       ).order_by('last_update')[:5]
            else:
                music_obj = Music.objects.filter(Q(share=True),
                                                 Q(name__icontains=query) | Q(artist__name__icontains=query) |
                                                 Q(language__icontains=query, music_type__icontains=query)
                                                 ).order_by('upload_time')[:5]
                album_obj = Album.objects.filter(Q(share=True),
                                                 Q(name__icontains=query) | Q(album_type__icontains=query) |
                                                 Q(description__icontains=query)
                                                 ).order_by('last_uploaded')[:5]
                playlist_obj = Playlist.objects.filter(Q(share=True),
                                                       Q(name__icontains=query) | Q(playlist_type__icontains=query)
                                                       ).order_by('last_update')[:5]
        else:
            context['category'] = True
            if self.request.user.is_authenticated:
                if category == 'music':
                    music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                     Q(name__icontains=query) | Q(artist__name__icontains=query) |
                                                     Q(language__icontains=query, music_type__icontains=query)
                                                     ).order_by('upload_time')
                elif category == 'album':
                    album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                     Q(name__icontains=query) | Q(album_type__icontains=query) |
                                                     Q(description__icontains=query)
                                                     ).order_by('last_uploaded')
                elif category == 'playlist':
                    playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                           Q(name__icontains=query) | Q(playlist_type__icontains=query)
                                                           ).order_by('last_update')
            else:
                if category == 'music':
                    music_obj = Music.objects.filter(Q(share=True),
                                                     Q(name__icontains=query) | Q(artist__name__icontains=query) |
                                                     Q(language__icontains=query, music_type__icontains=query)
                                                     ).order_by('upload_time')
                elif category == 'album':
                    album_obj = Album.objects.filter(Q(share=True),
                                                     Q(name__icontains=query) | Q(album_type__icontains=query) |
                                                     Q(description__icontains=query)
                                                     ).order_by('last_uploaded')
                elif category == 'playlist':
                    playlist_obj = Playlist.objects.filter(Q(share=True),
                                                           Q(name__icontains=query) | Q(playlist_type__icontains=query)
                                                           ).order_by('last_update')

        if music_obj:
            context['music_obj'] = music_obj
        if album_obj:
            context['album_obj'] = album_obj
        if playlist_obj:
            context['playlist_obj'] = playlist_obj
        context['search_q'] = query

        return context


class MusicShowAllView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(MusicShowAllView, self).get_context_data(**kwargs)
        context['category'] = True
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True)).order_by('upload_time')
        if music_obj:
            context['music_obj'] = music_obj
        return context


class AlbumShowAllView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumShowAllView, self).get_context_data(**kwargs)
        context['category'] = True
        if self.request.user.is_authenticated:
            album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('last_uploaded')
        else:
            album_obj = Album.objects.filter(Q(share=True)).order_by('last_uploaded')
        if album_obj:
            context['album_obj'] = album_obj
        return context


class PlaylistShowAllView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(PlaylistShowAllView, self).get_context_data(**kwargs)
        context['category'] = True
        if self.request.user.is_authenticated:
            playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user)).order_by('last_update')
        else:
            playlist_obj = Playlist.objects.filter(Q(share=True)).order_by('last_update')
        if playlist_obj:
            context['playlist_obj'] = playlist_obj
        return context


class ArtistView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistView, self).get_context_data(**kwargs)
        artist = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(artist__name__iexact=artist)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True),
                                             Q(artist__name__iexact=artist)).order_by('upload_time')
        album_obj = ''
        if music_obj:
            album_id = [music.album_id for music in music_obj if music.album_id]
            if self.request.user.is_authenticated:
                album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user), Q(id__in=album_id)).order_by('last_uploaded')
            else:
                album_obj = Album.objects.filter(Q(share=True), Q(id__in=album_id)).order_by('last_uploaded')
            context['music_obj'] = music_obj

        if album_obj:
            context['album_obj'] = album_obj

        context['artist'] = Artist.objects.filter(name__iexact=artist).first()
        print(Artist.objects.filter(name__iexact=artist).first())

        return context


class ArtistMusicView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistMusicView, self).get_context_data(**kwargs)
        artist = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(artist__name__iexact=artist)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True),
                                             Q(artist__name__iexact=artist)).order_by('upload_time')
        if music_obj:
            context['music_obj'] = music_obj

        context['artist'] = Artist.objects.filter(name__iexact=artist).first()
        context['category'] = True

        return context


class ArtistAlbumView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistAlbumView, self).get_context_data(**kwargs)
        artist = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(artist__name__iexact=artist)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True),
                                         Q(artist__name__iexact=artist)).order_by('upload_time')
        album_obj = ''
        if music_obj:
            album_id = [music.album_id for music in music_obj if music.album_id]
            if self.request.user.is_authenticated:
                album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user), Q(id__in=album_id)).order_by('last_uploaded')
            else:
                album_obj = Album.objects.filter(Q(share=True), Q(id__in=album_id)).order_by('last_uploaded')

        if album_obj:
            context['album_obj'] = album_obj

        context['artist'] = Artist.objects.filter(name__iexact=artist).first()
        context['category'] = True

        return context


class AlbumView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['album_view'] = True
        album_id = kwargs.get('id')
        album_obj = Album.objects.filter(id=album_id).first()
        if album_obj:
            music_obj = Music.objects.filter(album=album_id)
            context['music_obj'] = music_obj
            context['album_obj'] = album_obj
            context['album_no_of_music'] = music_obj.count()

        return context


class PlaylistView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(PlaylistView, self).get_context_data(**kwargs)
        context['album_view'] = True
        playlist_id = kwargs.get('id')
        playlist_obj = Playlist.objects.filter(id=playlist_id).first()
        playlist_id = [playlist_musc.song_id_id for playlist_musc in PlaylistMusic.objects.filter(playlist_id=playlist_id)]
        if playlist_id:
            music_obj = Music.objects.filter(id__in=playlist_id)
            context['music_obj'] = music_obj
            context['playlist_obj'] = playlist_obj
            context['album_no_of_music'] = music_obj.count()
        return context


class UploaderView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(UploaderView, self).get_context_data(**kwargs)
        uplaoder_id = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(uploaded_by=uplaoder_id)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True),
                                             Q(uploaded_by=uplaoder_id)).order_by('upload_time')
        album_obj = ''
        playlist_obj = ''
        if music_obj:
            context['music_obj'] = music_obj[:5]
            if self.request.user.is_authenticated:
                album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user), Q(uploaded_by=uplaoder_id)).order_by('last_uploaded')
                playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user), Q(uploaded_by=uplaoder_id)).order_by('last_update')
            else:
                album_obj = Album.objects.filter(Q(share=True), Q(uploaded_by=uplaoder_id)).order_by('last_uploaded')
                playlist_obj = Playlist.objects.filter(Q(share=True), Q(uploaded_by=uplaoder_id)).order_by('last_update')
        if album_obj:
            context['album_obj'] = album_obj[:5]
        if playlist_obj:
            context['playlist_obj'] = playlist_obj[:5]
        context['uploader'] = UserDetail.objects.filter(user=uplaoder_id).first()
        return context


class UploaderMusicView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(UploaderMusicView, self).get_context_data(**kwargs)
        uplaoder_id = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            music_obj = Music.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(uploaded_by=uplaoder_id)).order_by('upload_time')
        else:
            music_obj = Music.objects.filter(Q(share=True),
                                             Q(uploaded_by=uplaoder_id)).order_by('upload_time')
        if music_obj:
            context['music_obj'] = music_obj
        context['uploader'] = UserDetail.objects.filter(user=uplaoder_id).first()
        context['category'] = True
        return context


class UploaderAlbumView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(UploaderAlbumView, self).get_context_data(**kwargs)
        uplaoder_id = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            album_obj = Album.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                             Q(uploaded_by=uplaoder_id)).order_by('last_uploaded')
        else:
            album_obj = Album.objects.filter(Q(share=True),
                                             Q(uploaded_by=uplaoder_id)).order_by('last_uploaded')
        if album_obj:
            context['album_obj'] = album_obj
        context['uploader'] = UserDetail.objects.filter(user=uplaoder_id).first()
        context['category'] = True
        return context


class UploaderPlaylistView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(UploaderPlaylistView, self).get_context_data(**kwargs)
        uplaoder_id = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            playlist_obj = Playlist.objects.filter(Q(share=True) | Q(uploaded_by=self.request.user),
                                                   Q(uploaded_by=uplaoder_id)).order_by('last_update')
        else:
            playlist_obj = Playlist.objects.filter(Q(share=True),
                                                   Q(uploaded_by=uplaoder_id)).order_by('last_update')
        if playlist_obj:
            context['playlist_obj'] = playlist_obj
        context['uploader'] = UserDetail.objects.filter(user=uplaoder_id).first()
        context['category'] = True
        return context


class AddPlaylistMusic(DetailView):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            playlist_id = kwargs.get('playlist_id')
            music_id = kwargs.get('music_id')
            message = 'Already exist'
            if not PlaylistMusic.objects.filter(Q(playlist_id_id=playlist_id), Q(song_id_id=music_id)).exists():
                playlist_add_obj = PlaylistMusic()
                playlist_add_obj.playlist_id_id = playlist_id
                playlist_add_obj.song_id_id = music_id
                playlist_add_obj.save()
                message = 'Added to '+Playlist.objects.filter(id=playlist_id).first().name
            data = {
                'playlist_add_message': message,
            }
        return JsonResponse(data)