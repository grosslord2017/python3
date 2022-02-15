import json
from django.contrib import messages
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.http.response import JsonResponse

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .forms import AutorizationForm, EditProduct


def user_login(request):
    if request.method == 'POST':
        form = AutorizationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(
                username=form_data['username'],
                password=form_data['password']
            )
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('You are banned!')
            else:
                form.add_error(None, 'Unknown account')
                return render(request, 'user_app/login.html', {'form': form})
    else:
        form = AutorizationForm()
    return render(request, 'user_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def home_page(request):
    products_all = Product.objects.all()
    category_all = Category.objects.all()
    user = request.user
    return render(request, 'user_app/home.html', {'products': products_all, 'categories': category_all, 'user': user})

def product_info(request, pk):
    product = Product.objects.get(pk=pk)
    messages.add_message(request, messages.ERROR, 'YOUR ARE NOT ADMIN')
    return render(request, 'user_app/product_info.html', {'product': product})

def delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return HttpResponse('Delete complite')

def product_edit(request, pk):
    if request.user.is_superuser:
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            form = EditProduct(request.POST, instance=product)
            if form.is_valid():
                product.save()
                massage = f'Changes complite in {product.name}'
                return render(request, 'user_app/product_edit.html', {'form': form, 'massage': massage})
        else:
            form = EditProduct(instance=product)
        return render(request, 'user_app/product_edit.html', {'form': form, 'product': product})
    else:
        messages.add_message(request, messages.ERROR, 'YOUR ARE NOT ADMIN')
        return HttpResponseRedirect('/')

def category(request, name):
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category_fk_id=category.id)
    user = request.user
    return render(request, 'user_app/category.html', {'products': products, 'user': user})

def add_to_cart(request):
    # product_id = request.POST.get('product_id')
    product_id = json.loads(request.body).get('product_id')
    print(product_id)
    if product_id:
        product = Product.objects.get(id=product_id)
        cart = request.session.setdefault('cart', {})
        products = cart.setdefault('products', [])
        products.append(product_id)
        cart_total = cart.get('total') or 0
        product.quantity -= 1
        if product.quantity <= 0:
            product.is_active = False
        product.save()
        cart['total'] = cart_total + round(float(product.price), 2)
        request.session.modified = True
    # return HttpResponseRedirect('/')
        return JsonResponse({'qte': product.quantity})
    return JsonResponse({'error': 'Product not found'})

def cart(request):
    if request.user.username:
        try:
            session = request.session['cart']
            products = []
            for product_id in session['products']:
                count = session['products'].count(product_id)
                product = Product.objects.get(id=product_id)
                if [product, count] not in products:
                    products.append([product, count])

            return render(request, 'user_app/cart.html', {'products': products,
                                                           'total': session['total']})
        except:
            messages.add_message(request, messages.ERROR, 'Cart is Empty')
            return HttpResponseRedirect('/')
    else:
        messages.add_message(request, messages.ERROR, 'You are not logined')
        return HttpResponseRedirect('/')


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer