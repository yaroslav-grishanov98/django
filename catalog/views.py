from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from .models import Product, Category, ContactMessage
from .forms import ProductForm, ContactMessageForm
from .services import get_products_by_category

class IndexView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница каталога'
        context['welcome_message'] = 'Добро пожаловать в наш интернет-магазин!'

        context['latest_products'] = Product.objects.filter(status='published').order_by('-created_at')[:5]
        context['featured_categories'] = Category.objects.filter(is_active=True)[:3]

        context['special_offer'] = {
            'title': 'Специальное предложение!',
            'description': 'Скидки до 50% на все товары из новой коллекции',
            'end_date': '31 декабря 2025',
        }
        return context

class ContactsView(FormView):
    template_name = 'catalog/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('catalog:contacts')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['company_info'] = {
            'name': 'ООО "Интернет-магазин"',
            'address': 'г. Москва, ул. Примерная, д. 123',
            'phone': '+7 (123) 456-78-90',
            'email': 'info@example.com',
            'working_hours': 'Пн-Пт с 9:00 до 18:00',
        }
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        cache_key = 'product_list'
        products = cache.get(cache_key)
        if not products:
            products = Product.objects.filter(status='published').order_by('-created_at')
            cache.set(cache_key, products, 60 * 15)
        return products



@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(status='published')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm('catalog.change_product'):
            return Product.objects.all()

        return Product.objects.filter(
            Q(owner=self.request.user) &
            Q(status='draft')
        )

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user

        if form.instance.status == 'draft':
            form.instance.status = 'moderation'

        messages.success(self.request, 'Продукт отправлен на модерацию')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm('catalog.delete_product'):
            return Product.objects.all()

        return Product.objects.filter(
            Q(owner=self.request.user) &
            Q(status='draft')
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_unpublish_product'
    model = Product
    fields = ['status']
    template_name = 'catalog/product_moderation.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        if form.cleaned_data['status'] == 'rejected':
            messages.warning(self.request, 'Продукт отклонен от публикации')
        elif form.cleaned_data['status'] == 'published':
            messages.success(self.request, 'Продукт опубликован')
        return super().form_valid(form)


class ProductByCategoryView(ListView):
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = Category.objects.get(id=category_id)
        return context