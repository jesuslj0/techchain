from django import forms
from posts.models import Reel

class ReelCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = ['video', 'thumbnail', 'caption', 'is_public']
        widgets = {
            'video': forms.FileInput(attrs={'id': 'videoInput', 'accept': 'video/*'}),
            'thumbnail': forms.FileInput(attrs={'id': 'thumbnailInput', 'accept': 'image/*'}),
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'cols': 80,
                'placeholder': 'Escribe una descripción…'
            }),
            'is_public': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ReelCreateOrUpdateForm, self).__init__(*args, **kwargs)
        self.fields['caption'].required = False
        self.fields['thumbnail'].required = False
