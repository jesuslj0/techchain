from django import forms
from posts.models import Post, Tag

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'tags','title', 'content',]
        widgets = {
            'image': forms.FileInput(attrs={'id': 'imageInput'}),
            'tags': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={ 'rows': 5, 'cols':80 })
        }

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all();