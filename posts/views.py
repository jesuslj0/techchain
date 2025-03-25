from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from techchain.forms import PostCreateForm, CommentCreateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from notifications.utils import create_notification

@method_decorator(login_required, 'dispatch')
class PostsListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(user=self.request.user)
        return context
    

@method_decorator(login_required, 'dispatch')
class PostDetailView(DetailView, CreateView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.get_object())
        context["comments"] =  comments
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Comentario añadido.')
        return reverse('posts:detail', args=[self.get_object().pk])
    


@method_decorator(login_required, 'dispatch')
class PostsCreateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asigna el usuario actual al Post
        response = super().form_valid(form)     # ✅ Guarda el Post en la base de datos
        form.instance.tags.set(form.cleaned_data['tags'])  # ✅ Establece los tags después de guardar
        return response
    
    def get_success_url(self):
        return reverse_lazy('posts:list', kwargs={'user_id': self.object.user_id})
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = 'posts:detail'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Publicación eliminada correctamente.')
        return reverse_lazy('posts:list', kwargs={'user_id': self.object.user_id})

    def form_valid(self, form):
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    

# @login_required
# def like_post(request, pk):
#     post = Post.objects.get(pk=pk)

#     if request.user in post.likes.all():
#         messages.add_message(request, messages.INFO, message='Ya no te gusta esta publicación')
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#         messages.add_message(request, messages.INFO, message='Te gusta esta publicación')

#     return HttpResponseRedirect(reverse('posts:detail', args=[pk]))


@login_required
def like_post_ajax(request, pk):
    post = Post.objects.get(pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse (
            {
                'message': 'Ya no te gusta esta publicación',
                'nLikes': post.likes.count(),
                'liked': False,
            }
        )
    else:
        post.likes.add(request.user)

        if request.user != post.user: 
            msg = f'A {request.user.username} le a gustado tu publicación'
            link = reverse('posts:detail', args=[post.id])
            create_notification(post.user.profile, 'like', msg, link)

        return JsonResponse(
            {
                'message': 'Te gusta esta publicación',
                'nLikes': post.likes.count(),
                'liked': True,
            }
        )
