from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from profiles.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseñá',
            'password2': 'Confirma tu contraseña'
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
    
    # def clean_birth_date(self):
    #     birth_date = self.cleaned_data.get('birth_date')
    #     if birth_date:
    #         import datetime
    #         today = datetime.date.today()
    #         age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    #         if age < 16:
    #             raise ValidationError("Debes tener al menos 16 años para registrarte.")
    #     return birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password2'])
        user.save()
    
        return user
