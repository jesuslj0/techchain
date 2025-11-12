from django import forms
from posts.models import Post, Tag

class PostCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','title', 'content','tags']    
        widgets = {
            'image': forms.FileInput(attrs={'id': 'imageInput'}),
            'tags': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={ 'rows': 5, 'cols':80 })
        }
    
    def __init__(self, *args, **kwargs):
        super(PostCreateOrUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all();