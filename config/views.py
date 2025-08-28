from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    featured_categories = Category.objects.all()[:3]

    all_products = Product.objects.all()

    paginator = Paginator(all_products, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'title': 'Главная',
        'welcome_message': 'Добро пожаловать в наш каталог!',
        'featured_categories': featured_categories,
        'products': products,
        'special_offer': {
            'title': 'Специальное предложение!',
            'description': 'Скидка 20% на все товары до конца месяца.',
            'end_date': '31.12.2025'
        }
    }

    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """Контроллер для отображения детальной информации о товаре"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)

