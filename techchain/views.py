from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from techchain import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from posts.models import Post
from profiles.models import Follow, UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from .forms import ContactForm, LoginForm, RegisterForm
from .email import register_message
from django.core.mail import send_mail
from django.contrib.auth import login

# General Views
class HomeView(TemplateView):
    template_name = 'general/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            seguidos = Follow.objects.filter(follower=self.request.user.profile).values_list('followed__user', flat=True)
            posts = Post.objects.filter(user__profile__user__in=seguidos)
            # import ipdb; ipdb.set_trace()
            context["recent_posts"] = posts.order_by('created_at').reverse()
        else:
            context["recent_posts"] = Post.objects.all().order_by('created_at')[:10]
        
        return context


class ContactView(FormView):
    template_name = 'general/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact/')


class LegalView(TemplateView):
    template_name = 'general/legal.html'


class LoginView(LoginView): 
    template_name = 'general/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        remember_me = self.request.POST.get('remember_me')

        if user is not None:
            login(self.request, user)

            if remember_me:
                self.request.session.set_expiry(1209600)
            else:
                self.request.session.set_expiry(0)
                messages
            return HttpResponseRedirect(self.get_success_url())  # Redirige a la URL de éxito definida en el formulario
        else:
            return self.form_invalid(form)  # Si el usuario no se autentica, mostrar error

class LogoutView(LogoutView):
    template_name = 'general/logout.html'


class RegisterView(FormView): 
    template_name = 'general/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        user = form.save()
        
        messages.success(self.request, '¡Registro completado con éxito!')

        #Enviar correo de bienvenida
        register_message = "<h1>Bienvenido a TechChain</h1><p>Gracias por registrarte en nuestra plataforma.</p>"
        send_mail(
            subject="Registrado en Techchain",
            message="Gracias por registrarte en nuestra plataforma.",
            from_email="servicio.usuarios@techchain.live",
            recipient_list=[user.email],
            fail_silently=False,
            html_message=register_message
        )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrige los errores del formulario.')
        return super().form_invalid(form)
    
        
# Vista de exploración
class ExploreView(ListView):
    template_name = "general/explore.html"
    context_object_name = "posts" #Solo para posts (Queryset principal)
    
    def get_queryset(self):
        latest_posts = Post.objects.exclude(user=self.request.user).order_by('-created_at')
        return latest_posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        followed_users = Follow.objects.filter(follower=self.request.user.profile).values_list('followed', flat=True)
        new_users = UserProfile.objects.exclude(id__in=followed_users).exclude(user=self.request.user)[:5]  # Excluir al usuario actual

        context["users"] = new_users
        return context
    
