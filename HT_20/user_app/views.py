from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import AutorizationForm, EditProduct
from .models import Product, Category, Purchase


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
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditProduct(request.POST, instance=product)
        if form.is_valid():
            product.save()
            massage = f'Changes complite in {product.name}'
            return render(request, 'user_app/product_edit.html', {'form': form, 'massage': massage})
    else:
        form = EditProduct()
    return render(request, 'user_app/product_edit.html', {'form': form, 'product': product})

def category(request, name):
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category_fk_id=category.id)
    user = request.user
    return render(request, 'user_app/category.html', {'products': products, 'user': user})

def add_to_purchase(request, pk):
    item = Product.objects.get(pk=pk)
    try:
        book = Purchase.objects.get(item_id=item.id)
        book.count += 1
        book.save()
    except:
        Purchase.objects.create(customer=request.user, item=item, count=1)
    messages.add_message(request, messages.ERROR, 'item added to cart')
    return HttpResponseRedirect('/')

def purchase(request):
    try:
        carts = Purchase.objects.all()
        products = []

        for cart in carts:
            a = []
            product = Product.objects.get(id=cart.item_id)
            a.append(product)
            a.append(cart)
            products.append(a)

        return render(request, 'user_app/purchase.html', {'products': products})
    except:
        return HttpResponse('Cart is Empty')