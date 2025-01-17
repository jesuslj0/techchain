from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

# Contact Form

class ContactForm(forms.Form):
    subject = forms.CharField(label='Asunto', max_length=100)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea, )
    sender = forms.EmailField(label='Tu correo electrónico', required=True)
    cc_myself = forms.BooleanField(label='Quieres una copia?', required=False, )

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
    
    