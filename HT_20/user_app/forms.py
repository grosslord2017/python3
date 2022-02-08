from django.forms import ModelForm
from django import forms
from .models import Product


class AutorizationForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProduct(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'author', 'description', 'price', 'quantity', 'is_active']