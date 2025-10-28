from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .models import UserProfile, Follow
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse_lazy
from techchain.forms import UserProfileForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Follow
from posts.models import Post
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        user_uuid = self.kwargs['user_uuid']
        user = get_object_or_404(User, uuid=user_uuid)
        return get_object_or_404(UserProfile, user=user)

    def get_object(self):
        uuid_str = str(self.kwargs['user_uuid'])
        user = get_object_or_404(User, uuid=uuid_str)
        return get_object_or_404(UserProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.user.posts.all()
        context['posts'] = posts
        return context

class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'profiles/profile_update.html'
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Perfil actualizado correctamente!')
        return reverse_lazy('profiles:detail', kwargs={'user_uuid': self.request.user.uuid})

class ProfilesSearch(ListView):
    model = UserProfile
    template_name = 'profiles/profiles_search.html'
    context_object_name = "profiles"

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        
        if query:
            # Filtrar los perfiles que contienen el término de búsqueda en su nombre o en el campo que necesites
            profiles = UserProfile.objects.filter(user__username__icontains=query)
        else:
            # Si no hay búsqueda, mostrar todos los perfiles
            profiles = UserProfile.objects.all()

        # Obtener los perfiles que me siguen
        current_user = self.request.user.profile
        profiles_with_follow_date = []

        for profile in profiles:
            follow = Follow.objects.filter(follower=current_user, followed=profile).first()
            if follow:
                profiles_with_follow_date.append({
                    'profile': profile,
                    'profile_picture': profile.profile_picture,
                    'follow_up_date': follow.follow_up_date
                })
            else:
                profiles_with_follow_date.append({
                    'profile': profile,
                    'profile_picture': profile.profile_picture,
                    'follow_up_date': None
                })

        return profiles_with_follow_date
    
class FollowersView(ListView):
    model = Follow
    template_name = 'profiles/profiles_list_followers.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user_uuid = self.kwargs.get('user_uuid')
        return Follow.objects.filter(followed__user__uuid=user_uuid).select_related('follower', 'followed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_uuid = self.kwargs.get('user_uuid')
        context['user'] = get_object_or_404(UserProfile, user__uuid=user_uuid)
        return context
    
class FollowingView(ListView):
    model = Follow
    template_name = 'profiles/profiles_list_following.html'
    context_object_name = 'following'

    def get_queryset(self):
        user_uuid = self.kwargs.get('user_uuid')
        following = Follow.objects.filter(follower__user__uuid=user_uuid).select_related('followed')
        return following

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_uuid = self.kwargs.get('user_uuid')
        context['user'] = get_object_or_404(UserProfile, user__uuid=user_uuid)
        return context


#Cambio de contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'profiles/password_change.html'
    success_url = reverse_lazy('profiles:password_change_done')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        # Obtener la fecha del último cambio de contraseña
        last_change = user.profile.last_password_change
        
        if last_change and (now() - last_change) < timedelta(days=15):
            messages.warning(request, "Solo puedes cambiar tu contraseña cada 15 días. Último cambio realizado el {}".format(last_change.strftime('%d/%m/%Y')))
            return redirect('profiles:update', user.id)  # O redirigir a otro lado

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        # Guardar la nueva fecha del cambio de contraseña
        self.request.user.profile.last_password_change = now()
        self.request.user.profile.save()

        return response

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'profiles/password_change_done.html'


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@login_required
def toggle_follow(request, user_uuid):
    user_profile = get_object_or_404(UserProfile, user__uuid=user_uuid)
    if request.user.profile != user_profile:
        follow_record = Follow.objects.filter(follower=request.user.profile, followed=user_profile)
        if follow_record.exists():
            follow_record.delete()
        else:
            Follow.objects.create(follower=request.user.profile, followed=user_profile)
    return redirect('profiles:detail', user_uuid=user_uuid)

@login_required
@csrf_exempt  # 🔹 Permitir solicitudes AJAX sin CSRF manual
def toggle_privacy(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.private = not profile.private  # 🔹 Alternar estado
        profile.save()
        return JsonResponse({"status": "private" if profile.private else "public"})
    return JsonResponse({"error": "Método no permitido"}, status=405)
