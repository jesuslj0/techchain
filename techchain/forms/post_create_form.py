from django import forms
from posts.models import Post, Tag

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'tags','title', 'content',]
        widgets = {
            'image': forms.FileInput(attrs={'id': 'imageInput'}),
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={ 'rows': 3})
        }