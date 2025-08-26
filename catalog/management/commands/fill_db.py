from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Fills the database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Loading data from fixtures...')
        call_command('loaddata', 'catalog/fixtures/categories.json')
        call_command('loaddata', 'catalog/fixtures/products.json')

        electronics = Category.objects.get(name='Электроника')
        Product.objects.create(
            name='Планшет',
            description='Современный планшет для работы и развлечений',
            image='products/tablet.jpg',
            category=electronics,
            price=25000.00
        )

        self.stdout.write(self.style.SUCCESS('Successfully filled database with test data'))
