
from django import forms
from django.conf import settings
from userprofile.models import UserDetail, User
from .models import Album, Playlist, Music, Artist

MUSIC_TYPE_CHOICES = [
    ('rock', 'Rock'),
    ('pop', 'POP'),
    ('jazz', 'Jazz'),
    ('classical', 'Classical'),
    ('romantic', 'romantic'),
    ('festive', 'Festive'),
    ('mix', 'mix'),
    ('metal', 'metal'),
    ('rap', 'rap'),
    ('slow', 'slow'),
    ('sad', 'sad'),
]
LANGUAGE_CHOICE = [
    ('english', 'English'),
    ('hindi', 'Hindi'),
    ('bengali', 'Bengali'),
    ('oria', 'Oria'),
    ('panjabi', 'Panjabi'),
    ('spanish', 'Spanish'),
]


# update user details "name, email, profile picture"
class UserUpdateForm(forms.Form):
    user = forms.CharField(max_length=200, widget=forms.HiddenInput)
    name = forms.CharField(max_length=150, label='Full Name')
    email = forms.EmailField(label='Email')
    user_image = forms.ImageField(label='Select Image', required=False)


# create new Album
class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description', 'album_type', 'share', 'album_cover', ]
        labels = {
            'name': 'Album Name',
            'description': 'Description',
            'album_type': 'Type',
            'share': 'Share',
            'album_cover': 'Upload Cover',
        }
        widgets = {
            'share': forms.CheckboxInput(attrs={'class': 'upload-input-check'}),
            'description': forms.Textarea(),
            'album_type': forms.Select(choices=MUSIC_TYPE_CHOICES),
        }


# Create New Playlist
class PlaylistCreateForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'playlist_type', 'share', 'playlist_cover', ]
        labels = {
            'name': 'Playlist Name',
            'playlist_type': 'Type',
            'share': 'Share',
            'playlist_cover': 'Playlist Cover',
        }
        widgets = {
            'share': forms.CheckboxInput(attrs={'class': 'upload-input-check'}),
            'playlist_type': forms.Select(choices=MUSIC_TYPE_CHOICES),
        }


# Upload new Music
class MusicUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.extra_info = kwargs.pop('extra_info')
        super(MusicUploadForm, self).__init__(*args, **kwargs)
        self.ALBUM_CHOICE = self.make_choice()
        self.fields['album'].choices = self.ALBUM_CHOICE
        self.fields['file'].widget.attrs.update({'accept': '.mp3'})

    def make_choice(self):
        album_list = []
        if not self.extra_info.get('album_id'):
            album_qs = Album.objects.filter(uploaded_by=self.extra_info.get('user'))
            album_list = [(None, None)]
        else:
            album_qs = Album.objects.filter(id=self.extra_info.get('album_id'))

        for album in album_qs:
            album_list.append(tuple([album.id, album.name]))
        return album_list

    album = forms.Select()

    class Meta:
        model = Music
        fields = ['name', 'album', 'artist', 'music_type', 'language', 'share', 'file', 'music_cover']
        labels = {
            'name': 'Music Name',
            'album': 'Album',
            'artist': 'Artist',
            'music_type': 'Type',
            'language': 'Language',
            'share': 'Share',
            'file': 'Music File',
            'music_cover': 'Cover',
        }
        widgets = {
            'share': forms.CheckboxInput(attrs={'class': 'upload-input-check'}),
            'music_type': forms.Select(choices=MUSIC_TYPE_CHOICES),
            'language': forms.Select(choices=LANGUAGE_CHOICE),
        }

    def clean_file(self):
        audio_file = self.cleaned_data.get('file').name
        if not audio_file.lower().endswith(('.mp3',)):
            raise forms.ValidationError('Not a mp3 file')
        return self.cleaned_data.get('file')


class ArtistCreateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'about', 'artist_image']
        labels = {
            'name': 'Artist Name',
            'about': 'About',
            'artist_image': 'Image',
        }
        widgets = {
            'about': forms.Textarea(),
        }