from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Usuario o Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            # Intentar buscar al usuario por email o username
            user = User.objects.filter(email=username_or_email).first()
            if not user:
                user = User.objects.filter(username=username_or_email).first()

            if user:
                authenticated_user = authenticate(username=user.username, password=password)
                if authenticated_user is None:
                    raise forms.ValidationError("Credenciales incorrectas.")
                else:
                    self.user_cache = authenticated_user  # Guardar el usuario autenticado
            else:
                raise forms.ValidationError("Usuario no encontrado.")

        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache 