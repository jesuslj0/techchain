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
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Fecha de nacimiento")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2', 'profile_picture', 'bio']
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
            'birth_date': 'Fecha de nacimiento',
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
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            import datetime
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 16:
                raise ValidationError("Debes tener al menos 16 años para registrarte.")
        return birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password2'])
        user.save()
        
        profile_picture = self.cleaned_data['profile_picture']
        bio = self.cleaned_data['bio']
        birth_date = self.cleaned_data['birth_date']
        UserProfile.objects.create(
            user=user,
            bio=bio,
            birth_date=birth_date,
            profile_picture=profile_picture
        )
    
        return user
