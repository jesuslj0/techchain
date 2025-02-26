from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

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

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password1')
        password_confirm = self.cleaned_data.get('password2')
        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email
    
    def save(self, commit=True): #Guardar en la base de datos
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']

        user.save()
        # Crear el perfil de usuario asociado
        UserProfile.objects.create(
            user=user,
            bio=self.cleaned_data['bio'],
            profile_picture=self.cleaned_data.get('profile_picture', None)
        )
        
        return user
