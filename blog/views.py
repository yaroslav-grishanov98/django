from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin


class BlogPostListView(ListView):
    """Представление для отображения списка записей блога"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Представление для просмотра отдельной записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        obj.views_count += 1

        if obj.views_count == 100:
            send_mail(
                'Поздравляем с достижением!',
                f'Статья "{obj.title}" достигла 100 просмотров!',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
                [settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else 'admin@example.com'],
                fail_silently=True,
            )

        obj.save()

        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания новой записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    """Представление для редактирования существующей записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    login_url = reverse_lazy('users:login')

    def test_func(self):
        post = self.get_object()
        return (
                self.request.user == post.author or
                self.request.user.groups.filter(name='Контент-менеджеры').exists() or
                self.request.user.is_staff
        )

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    """Представление для удаления записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        post = self.get_object()
        return (
                self.request.user == post.author or
                self.request.user.groups.filter(name='Контент-менеджеры').exists() or
                self.request.user.is_staff
        )
