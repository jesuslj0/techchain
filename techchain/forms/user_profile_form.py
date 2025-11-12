from django import forms
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'profile_picture', 'bio', 'private']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'data-id': 'privateButton'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if profile.user:
            profile.user.username = self.cleaned_data['username']
            if commit:
                profile.user.save()
        if commit:
            profile.save()
        return profile