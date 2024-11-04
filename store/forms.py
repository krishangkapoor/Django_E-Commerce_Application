from django import forms
from .models import Product, ProductImage
from .widgets import MultipleFileInput

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': MultipleFileInput()
        }

