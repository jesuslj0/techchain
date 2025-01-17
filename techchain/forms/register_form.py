from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirma tu contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email
