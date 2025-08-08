from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def index(request):
    """
    Контроллер для отображения домашней страницы
    """
    context = {
        'title': 'Главная страница каталога',
        'welcome_message': 'Добро пожаловать в наш интернет-магазин!',
        'featured_categories': [
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
        ],
        'special_offer': {
            'title': 'Специальное предложение!',
            'description': 'Скидки до 50% на все товары из новой коллекции',
            'end_date': '31 декабря 2023',
        }
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """Контроллер для отображения страницы с контактной информацией и обработки формы обратной связи"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('catalog:contacts')
    else:
        form = ContactForm()

    context = {
        'title': 'Контакты',
        'company_info': {
            'name': 'ООО "Интернет-магазин"',
            'address': 'г. Москва, ул. Примерная, д. 123',
            'phone': '+7 (123) 456-78-90',
            'email': 'info@example.com',
            'working_hours': 'Пн-Пт с 9:00 до 18:00',
        },
        'map_url': 'https://maps.google.com/...',
        'social_media': [
            {'name': 'Facebook', 'url': 'https://facebook.com/...'},
            {'name': 'Instagram', 'url': 'https://instagram.com/...'},
            {'name': 'Twitter', 'url': 'https://twitter.com/...'},
        ],
        'form': form,
    }
    return render(request, 'catalog/contacts.html', context)

