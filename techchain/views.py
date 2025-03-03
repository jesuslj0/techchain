from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from techchain import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from posts.models import Post
from profiles.models import Follow, UserProfile
from django.contrib import messages
from .forms import RegisterForm
from .email import register_message
from django.core.mail import send_mail

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
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact/')


class LegalView(TemplateView):
    template_name = 'general/legal.html'


class LoginView(LoginView): 
    template_name = 'general/login.html'
    authentication_form = forms.LoginForm
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

class LogoutView(LogoutView):
    template_name = 'general/logout.html'


class RegisterView(FormView): 
    template_name = 'general/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirige a la página de inicio de sesión después de un registro exitoso

    def form_valid(self, form):
        # Guarda el usuario pero no lo confirma aún
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password2'])  # Encripta la contraseña
        user.save()  # Guarda el usuario en la base de datos
        messages.success(self.request, '¡Registro completado con éxito!')

        #Enviar correo de bienvenida
        send_mail(
            subject="Bienvenido a TechChain",
            message="Gracias por registrarte en nuestra plataforma.",  # Fallback en texto plano
            from_email="servicio.usuarios@techchain.live",
            recipient_list=[user.email],
            fail_silently=False,
            html_message=register_message  # Correo en HTML
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
    
