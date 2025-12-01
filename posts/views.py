from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from techchain.forms import PostCreateOrUpdateForm, CommentCreateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from notifications.utils import create_notification
from notifications.models import LikeLog
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from profiles.models import User

@method_decorator(login_required, 'dispatch')
class PostsListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_uuid = self.kwargs.get('user_uuid', None)
        if user_uuid:
            context["posts"] = Post.objects.filter(user__uuid=user_uuid).order_by('-created_at')
        else:
            context["posts"] = Post.objects.filter(user=self.request.user).order_by('-created_at')
        
        user = User.objects.get(uuid=user_uuid)
        context['user_obj'] = user
        return context
    

@method_decorator(login_required, 'dispatch')
class PostDetailView(DetailView, CreateView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = (
            Comment.objects.filter(post=self.get_object())
            .annotate(num_likes=Count('likes', distinct=True))
            .order_by("-num_likes", "created_at")
        )
        context["comments"] =  comments
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Comentario añadido.')
        return reverse('posts:detail', args=[self.get_object().pk])
    

@method_decorator(login_required, name='dispatch')
class PostCreateOrUpdateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    form_class = PostCreateOrUpdateForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Post.objects.filter(pk=pk, user=self.request.user).first()
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return self.render_to_response({'form': form})

    def get_success_url(self):
        return reverse('posts:list', kwargs={'user_uuid': str(self.request.user.uuid)})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return redirect(self.get_success_url())
        return self.render_to_response({'form': form})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = 'posts:detail'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Publicación eliminada correctamente.')
        return reverse_lazy('posts:list', kwargs={'user_uuid': str(self.object.user.uuid)})

    def form_valid(self, form):
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    

@login_required
def like_post_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        LikeLog.objects.filter(user=user, post=post).delete()
        return JsonResponse({
            'message': 'Ya no te gusta esta publicación',
            'nLikes': post.likes.count(),
            'liked': False,
        })
    
    post.likes.add(user)

    cooldown_minutes = 10
    like_log, created = LikeLog.objects.get_or_create(user=user, post=post)

    # Si ya existía el registro, comprobar cooldown
    if not created:
        time_since = timezone.now() - like_log.timestamp
        if time_since < timedelta(minutes=cooldown_minutes):
            # En cooldown, no enviar notificación ni actualizar timestamp
            return JsonResponse({
                'message': 'Te gusta esta publicación',
                'nLikes': post.likes.count(),
                'liked': True,
            })

    # Fuera de cooldown o es un nuevo like -> actualizar timestamp
    like_log.timestamp = timezone.now()
    like_log.save()

    # Enviar notificación solo si no es auto-like
    if user != post.user:
        msg = f'A {user.username} le ha gustado tu publicación'
        link = reverse('posts:detail', args=[post.id])
        create_notification(post.user.profile, 'like', post, msg, link)

    return JsonResponse({
        'message': 'Te gusta esta publicación',
        'nLikes': post.likes.count(),
        'liked': True,
    })

@login_required
def like_comment_ajax(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        return JsonResponse({
            'message': 'Ya no te gusta este comentario',
            'nLikes': comment.likes.count(),
            'liked': False,
        })

    comment.likes.add(user)

    return JsonResponse({
        'message': 'Te gusta este comentario',
        'nLikes': comment.likes.count(),
        'liked': True,
    })