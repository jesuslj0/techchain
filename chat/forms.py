from django import forms
from .models import GroupChatRoom

class GroupChatForm(forms.ModelForm):
    name = forms.CharField(label='Nombre del grupo', max_length=255)
    description = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={"rows": 3}))
    image = forms.FileField(label="Imagen de grupo", allow_empty_file=True, required=False)
    users = forms.ModelMultipleChoiceField(
        queryset=None,
        label="Miembros",
        widget=forms.SelectMultiple(attrs={'class': 'django-select2', 'data-placeholder': 'Selecciona participantes...'}),
    )

    class Meta:
        model = GroupChatRoom
        fields = ['name', 'description', 'users', 'image']

    def __init__(self, *args, **kwargs):
        allowed_users = kwargs.pop('allowed_users', None)
        super().__init__(*args, **kwargs)
        if allowed_users is not None:
            self.fields['users'].queryset = allowed_users
