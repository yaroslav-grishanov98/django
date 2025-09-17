from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Category, Product
from django.core.management import call_command
from django.contrib.auth import get_user_model
from blog.models import BlogPost

User = get_user_model()

class Command(BaseCommand):
    help = 'Fills the database with test data and creates moderator groups'

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
            price=25000.00,
            status='draft'
        )

        self.stdout.write('Creating moderator group...')
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        product_content_type = ContentType.objects.get_for_model(Product)

        try:
            unpublish_permission = Permission.objects.get(
                content_type=product_content_type,
                codename='can_unpublish_product'
            )
            delete_permission = Permission.objects.get(
                content_type=product_content_type,
                codename='delete_product'
            )

            moderator_group.permissions.add(
                unpublish_permission,
                delete_permission
            )
            self.stdout.write(self.style.SUCCESS('Группа модераторов продуктов создана успешно'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не удалось найти необходимые разрешения для продуктов'))

        self.stdout.write('Creating content manager group...')
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджеры')

        blog_content_type = ContentType.objects.get_for_model(BlogPost)

        try:
            change_blog_permission = Permission.objects.get(
                content_type=blog_content_type,
                codename='change_blogpost'
            )
            delete_blog_permission = Permission.objects.get(
                content_type=blog_content_type,
                codename='delete_blogpost'
            )

            content_manager_group.permissions.add(
                change_blog_permission,
                delete_blog_permission
            )
            self.stdout.write(self.style.SUCCESS('Группа контент-менеджеров создана успешно'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не удалось найти необходимые разрешения для блога'))

        try:
            moderator, created = User.objects.get_or_create(
                email='moderator@example.com',
                defaults={
                    'username': 'moderator',
                    'is_staff': True
                }
            )
            if created:
                moderator.set_password('moderator_password')
                moderator.save()
                moderator.groups.add(moderator_group)
                self.stdout.write(self.style.SUCCESS('Тестовый модератор продуктов создан'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания модератора продуктов: {e}'))

        try:
            content_manager, created = User.objects.get_or_create(
                email='content_manager@example.com',
                defaults={
                    'username': 'content_manager',
                    'is_staff': True
                }
            )
            if created:
                content_manager.set_password('content_manager_password')
                content_manager.save()
                content_manager.groups.add(content_manager_group)
                self.stdout.write(self.style.SUCCESS('Тестовый контент-менеджер создан'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания контент-менеджера: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully created all groups and test users'))
