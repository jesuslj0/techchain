from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

# Contact Form

class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Asunto',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Reportar un error'}),
    )
    sender = forms.EmailField(
        label='Tu correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'tucorreo@ejemplo.com'}),
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Cuéntanos en qué podemos ayudarte…',
        }),
    )
    cc_myself = forms.BooleanField(
        label='Enviarme una copia a mi correo',
        required=False,
    )

    def clean_data(self):
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]
        sender = self.cleaned_data["sender"]
        cc_myself = self.cleaned_data["cc_myself"]

        recipients = ["info@example.com"]
        if cc_myself:
            recipients.append(sender)

        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect("/thanks/")
    
    