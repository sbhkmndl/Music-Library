from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView
from django.http import Http404
# Create your views here.
from musiccreate.models import Album, PlaylistMusic, Playlist, Music


# Login required Mixin
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)


class UserDetailsView(LoginRequiredMixin,TemplateView):
    template_name = 'edit/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        user_detail_obj = user_obj.user_set
        context['username'] = user_obj.username
        context['name'] = user_detail_obj.name
        context['email'] = user_obj.email
        try:
            context['prof_img'] = user_detail_obj.user_image.url
        except:
            pass
        return context


class MusicEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit/music_edit.html'

    def get_context_data(self, **kwargs):
        context = super(MusicEditView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        music_obj = user_obj.upload_musics.all()
        context['category'] = 'Music'
        if music_obj:
            context['musics'] = music_obj
        return context


class AlbumEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit/album_edit.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumEditView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        album_obj = user_obj.upload_albums.all()
        context['category'] = 'Album'
        if album_obj:
            context['albums'] = album_obj
        return context


class PlaylistEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit/playlist_edit.html'

    def get_context_data(self, **kwargs):
        context = super(PlaylistEditView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        playlist_obj = user_obj.upload_playlists.all()
        context['category'] = 'Playlist'
        if playlist_obj:
            context['playlists'] = playlist_obj
        return context


class AlbumMusicEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit/music_edit.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumMusicEditView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        id = kwargs.get('id')
        music_obj = user_obj.upload_musics.filter(album=id)
        if music_obj:
            context['musics'] = music_obj
        if Album.objects.all():
            context['category'] = Album.objects.filter(id=id).first().name
        context['album'] = True
        return context


class PlaylistMusicEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit/music_edit.html'

    def get_context_data(self, **kwargs):
        context = super(PlaylistMusicEditView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        id = kwargs.get('id')
        playlist_obj = PlaylistMusic.objects.select_related('song_id').filter(playlist_id=id)
        playlist_ids = []
        for playlist_temp in playlist_obj:
            playlist_ids.append(playlist_temp.song_id.id)
        print(playlist_ids)
        music_obj = Music.objects.filter(Q(id__in=playlist_ids),
                                         Q(share=True) | Q(uploaded_by=user_obj))
        context['musics'] = music_obj
        context['category'] = Playlist.objects.filter(id=id).first().name
        context['playlist'] = id
        return context


class MusicDeleteView(LoginRequiredMixin, DeleteView):
    model = Music

    def get_success_url(self):
        messages.success(self.request, 'successfully Deleted')
        return reverse('music_edit')

    def get_context_data(self, **kwargs):
        context = super(MusicDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Music Delete'
        context['cancel'] = '/edit/music'
        return context


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album

    def get_success_url(self):
        messages.success(self.request, 'successfully Deleted')
        return reverse('album_edit')

    def get_context_data(self, **kwargs):
        context = super(AlbumDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Album Delete'
        context['cancel'] = '/edit/album'
        return context


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist

    def get_success_url(self):
        messages.success(self.request, 'successfully Deleted')
        return reverse('playlist_edit')

    def get_context_data(self, **kwargs):
        context = super(PlaylistDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Playlist Delete'
        context['cancel'] = '/edit/playlist'
        return context


class PlaylistMusicDeleteView(DeleteView):
    model = PlaylistMusic

    def get_success_url(self):
        messages.success(self.request, 'successfully Deleted')
        return reverse('playlist_edit')

    def get_context_data(self, **kwargs):
        context = super(PlaylistMusicDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Playlist Content Delete'
        context['cancel'] = '/edit/playlist'
        return context
