from django import forms
import os
from django.core.exceptions import ValidationError
from .models import Product, ContactMessage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = 'form-control'

            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.FileInput):
                css_class = 'form-control form-control-file'

            field.widget.attrs.update({
                'class': css_class,
                'placeholder': f'Введите {field.label.lower()}' if field_name != 'image' else 'Выберите изображение',
            })

            if field_name == 'description':
                field.widget.attrs.update({
                    'rows': 4,
                    'style': 'resize: vertical;',
                })

            if field_name == 'price':
                field.widget.attrs.update({
                    'min': '0',
                    'step': '0.01',
                })

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                           'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название не может содержать запрещенное слово '{word}'")

        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                           'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Описание не может содержать запрещенное слово '{word}'")

        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if not image and self.instance.pk:
            return self.instance.image

        if not image and not self.instance.pk:
            if self.fields['image'].required:
                raise forms.ValidationError("Необходимо загрузить изображение продукта")
            return image

        ext = os.path.splitext(image.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in valid_extensions:
            raise forms.ValidationError("Поддерживаются только изображения в формате JPEG или PNG")

        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise forms.ValidationError("Размер изображения не должен превышать 5 МБ")

        return image

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваше сообщение'})
        }
