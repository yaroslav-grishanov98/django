from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


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


class BlogPostCreateView(CreateView):
    """Представление для создания новой записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    """Представление для редактирования существующей записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Представление для удаления записи блога"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
