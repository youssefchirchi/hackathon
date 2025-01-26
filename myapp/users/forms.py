from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_type', 'file', 'file_path']

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})



from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), label="Entrez votre message")
