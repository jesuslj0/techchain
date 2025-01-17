from django import forms
from posts.models import Comment
from crispy_forms.helper import FormHelper

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels ={
            'text': 'Comenta aquí',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.label_suffix = ''