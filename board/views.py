from datetime import datetime, timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import mail_managers, send_mail
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .forms import PostsForm, CommentsForm
from .models import Posts, Categories, Comment
from django.db.models.signals import post_save

# from .filters import CategoriesFilter
# @receiver(post_save, sender=Comment)
# def notify_managers_comments(sender, instance, created, **kwargs):
#     if created:
#         subject = f' Написал комментарий {instance.link_2} {instance.time_in_comment("%d %m %Y")} '
#
#     mail_managers(subject=subject, message=f'Добавлен комментарий {instance.text_comment}',)

class PostsViews(ListView):
    model = Posts
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


"""Для добавление в обьявление комментариев добавляем в наследование FormMixin и добавляем поле с формой form_class = CommentsForm """
class PostsDetailViews(FormMixin,DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentsForm
    # success_url = reverse_lazy('post_detail')

def create_comment(request, pk):
    post = get_object_or_404(Posts,id=pk)
    comment = Comment.objects.filter(link_1=pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.link_2 = request.user
            form.link_1 = post
            form.save()
            # отправляем письмо
            send_mail(
                subject=f'{form.link_2} {form.time_in_comment}',
                # имя клиента и дата записи будут в теме для удобства
                message=f'Комментарий: {form.text_comment} Пользователь:{form.link_2} Объявление:{form.link_1}',  # сообщение с кратким описанием проблемы
                from_email='Viteeek91.90@yandex.ru',
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                recipient_list=[form.link_2.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
            )
            return redirect('post_detail', pk)
    else:
        form = CommentsForm()
                # return HttpResponseRedirect('/posts/<int:pk>')
    return render(request, 'post.html', {'post': post, 'form': form,'comments': comment})



""" Это представление на форму создание публикации """
def create_posts(request):
    form = PostsForm()

    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/posts/')

    return render(request, 'posts_form.html', {'form': form})



# Добавляем новое представление для создания постов.
class PostsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostsForm
    # модель постов
    model = Posts
    # и новый шаблон, в котором используется форма.
    template_name = 'posts_form.html'

class PostsUpdate(LoginRequiredMixin,UpdateView):
    form_class = PostsForm
    model = Posts
    template_name = 'posts_form.html'

class PostsDelete(DeleteView):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')





# class CommentCreate(CreateView):
#     # Указываем нашу разработанную форму
#     form_class = CommentsForm
#     # модель постов
#     model = Comment
#     # и новый шаблон, в котором используется форма.
#     context_object_name = 'comment'
#     template_name = 'posts_form.html'

    # def create_posts(request):
    #     form = CommentsForm()
    #
    #     if request.method == 'POST':
    #         form = CommentsForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect('/posts/')
    #
    #     return render(request, 'posts_form.html', {'form': form})

# class CommentsDelete(DeleteView):
#     model = Comment
#     template_name = 'comment_delete.html'
#     success_url = reverse_lazy('posts_list')