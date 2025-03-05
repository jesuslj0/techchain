from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .models import UserProfile, Follow
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from techchain.forms import UserProfileForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Follow
from posts.models import Post

# Create your views here.
class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.user.posts.all
        context['posts'] = posts
        return context

class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'profiles/profile_update.html'
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    form_class = UserProfileForm
    
    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'user_id': self.object.user_id})

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
        # Obtener el usuario actual a través del parámetro de la URL
        user_id = self.kwargs.get('user_id')
        # Filtrar los seguidores de ese usuario
        return Follow.objects.filter(followed__id=user_id).select_related('follower', 'followed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir el usuario actual al contexto
        user_id = self.kwargs.get('user_id')
        context['user'] = get_object_or_404(UserProfile, id=user_id)
        return context
    
class FollowingView(ListView):
    model = Follow
    template_name = 'profiles/profiles_list_following.html'
    context_object_name = 'following'

    def get_queryset(self):
        # Obtener el usuario actual a través del parámetro de la URL
        user_id = self.kwargs.get('user_id')
        # Filtrar los seguidos por ese usuario
        following = Follow.objects.filter(follower__id=user_id).select_related('followed')
        return following
        # Envia directamente los objetos de following al contexto
        #Debugg
                # for i in context['following']:
                #     print(i.followed.user.username)
                #     print('le sigues desde')
                #     print(i.follow_up_date)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir el usuario actual al contexto
        user_id = self.kwargs.get('user_id')
        context['user'] = get_object_or_404(UserProfile, id=user_id)
        return context

@login_required
def toggle_follow(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    if request.user.profile != user_profile:
        # Comprobar si ya está siguiendo
        follow_record = Follow.objects.filter(follower=request.user.profile, followed=user_profile)

        if follow_record.exists():
            # Si ya está siguiendo, eliminar el seguimiento
            follow_record.delete()
        else:
            # Si no está siguiendo, crear un nuevo seguimiento
            Follow.objects.create(follower=request.user.profile, followed=user_profile)

    return redirect('profiles:detail', user_id=user_id)

#Cambio de contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'profiles/password_change.html'
    success_url = reverse_lazy('profiles:password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'profiles/password_change_done.html'