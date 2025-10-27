from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from profiles.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=True)
    profile_picture = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_picture', 'bio']
        widgets = {
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'profile_picture': forms.ClearableFileInput(),
            'bio': forms.Textarea(),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'password1': 'Contraseñá',
            'password2': 'Confirma tu contraseñá',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'profile_picture': 'Imagen de perfil',
            'bio': 'Información sobre ti',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password2'])
        
        user.save()
        profile_picture = self.cleaned_data['profile_picture']
        bio = self.cleaned_data['bio']
        UserProfile.objects.create(
            user=user,
            bio=bio,
            profile_picture=profile_picture
        )
    
        return user
