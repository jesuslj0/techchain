from django import forms
from posts.models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'imageInput'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }