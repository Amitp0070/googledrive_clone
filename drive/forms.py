from django import forms
from .models import File, Folder
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['parent'].queryset = Folder.objects.filter(owner=user, is_trash=False)

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FolderForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['parent'].queryset = Folder.objects.filter(owner=user, is_trash=False)

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class ShareForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )