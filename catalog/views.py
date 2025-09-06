from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product
from .forms import ContactForm, ProductForm

class IndexView(TemplateView):
    """Класс для отображения домашней страницы с последними продуктами"""
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница каталога'
        context['welcome_message'] = 'Добро пожаловать в наш интернет-магазин!'
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]
        context['featured_categories'] = [
            {
                'name': 'Электроника',
                'description': 'Смартфоны, ноутбуки, планшеты и другие гаджеты',
                'image_url': '#',
            },
            {
                'name': 'Одежда',
                'description': 'Мужская, женская и детская одежда',
                'image_url': '#',
            },
            {
                'name': 'Книги',
                'description': 'Художественная литература, учебники, журналы',
                'image_url': '#',
            },
        ]
        context['special_offer'] = {
            'title': 'Специальное предложение!',
            'description': 'Скидки до 50% на все товары из новой коллекции',
            'end_date': '31 декабря 2023',
        }
        return context


class ContactsView(FormView):
    """Класс для отображения страницы с контактной информацией и обработки формы обратной связи"""
    template_name = 'catalog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contacts')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
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
        context['map_url'] = 'https://maps.google.com/...'
        context['social_media'] = [
            {'name': 'Вконтакте', 'url': 'https://vk.com/...'},
            {'name': 'Instagram', 'url': 'https://instagram.com/...'},
            {'name': 'Телеграмм', 'url': 'https://web.telegram.org/a/...'},
        ]
        return context


class ProductListView(ListView):
    """Класс для отображения списка товаров"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Класс для отображения детальной информации о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Класс для создания нового товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """Класс для обновления существующего товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class ProductDeleteView(DeleteView):
    """Класс для удаления товара"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)
