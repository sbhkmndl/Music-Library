from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, FormView, CreateView
from django.conf import settings
from .forms import UserUpdateForm, AlbumCreateForm, PlaylistCreateForm, MusicUploadForm, ArtistCreateForm
from userprofile.models import UserDetail, User
from .models import Album, Playlist, Music


# Create your views here.

# Login required Mixin
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)


# User Update view
class UserUpdateView(LoginRequiredMixin, FormView):
    form_class = UserUpdateForm
    template_name = 'upload/edit_profile.html'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            update_user = User.objects.filter(id=form.cleaned_data.get('user')).first()
            update_details = UserDetail.objects.filter(user=update_user).first()
            update_user.email = form.cleaned_data.get('email')
            update_details.name = form.cleaned_data.get('name')
            if form.cleaned_data.get('user_image'):
                update_details.user_image = form.cleaned_data.get('user_image')
            update_user.save()
            update_details.save()
            messages.success(self.request, 'Successfully Updated')
            return HttpResponseRedirect('/edit/user/')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        current_user = request.user
        current_user_details = current_user.user_set
        context = self.get_context_data()
        try:
            context['profile_pic'] = current_user_details.user_image.url
        except:
            pass
        return self.render_to_response(context)

    def get_initial(self):
        current_user = self.request.user
        current_user_details = current_user.user_set
        return {
            'user': current_user_details.id,
            'name': current_user_details.name,
            'email': current_user.email,
        }

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context


# Album create
class AlbumCreateView(LoginRequiredMixin, CreateView):
    form_class = AlbumCreateForm
    template_name = 'upload/create_album.html'
    model = Album

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Successfully Created')
        return reverse('album_edit')

    def get_context_data(self, **kwargs):
        context = super(AlbumCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Album Create'
        return context


# Playlist Create
class PlaylistCreateView(LoginRequiredMixin, CreateView):
    form_class = PlaylistCreateForm
    template_name = 'upload/create_playlist.html'
    model = Playlist

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super(PlaylistCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Successfully Created')
        return reverse('playlist_edit')

    def get_context_data(self, **kwargs):
        context = super(PlaylistCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Playlist Create'
        return context


# Upload new music
class MusicUploadView(LoginRequiredMixin, CreateView):
    form_class = MusicUploadForm
    template_name = 'upload/upload_song.html'
    model = Music

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super(MusicUploadView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Successfully Uploaded')
        return reverse('music_edit')

    def get_context_data(self, **kwargs):
        context = super(MusicUploadView, self).get_context_data(**kwargs)
        context['title'] = 'Music Upload'
        return context

    # send user details to form.py(MusicUploadForm)
    def get_form_kwargs(self):
        kwargs = super(MusicUploadView, self).get_form_kwargs()
        extra_info = {}
        extra_info['user'] = self.request.user
        try:
            extra_info['album_id']= self.kwargs.get('album_id')
        except:
            pass
        kwargs.update({'extra_info': extra_info})
        return kwargs


# Create new artist
class ArtistCreateView(LoginRequiredMixin, CreateView):
    form_class = ArtistCreateForm
    template_name = 'upload/create_artist.html'

    def get_success_url(self):
        messages.success(self.request, 'Successfully Added')
        print(messages)
        return reverse('upload_music')

    def get_context_data(self, **kwargs):
        context = super(ArtistCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Artist Add'
        return context
