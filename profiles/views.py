from django.views.generic import DetailView, ListView, UpdateView
from .models import UserProfile, Follow
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from instagram.forms import UserProfileForm
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
    template_name = 'profiles/profiles_list.html'
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
        context['user'] = User.objects.get(id=user_id)
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

