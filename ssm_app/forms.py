from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from ssm_app.models import Playlist


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = '__all__'
        exclude = ['user']
        # labels = {
        #     'name': 'Write your playlist name here'
        # }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Write your playlist name here'
            }),
        }




class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
