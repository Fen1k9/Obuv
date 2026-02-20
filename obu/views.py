from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import User, Product
from  django.db.models import  Q

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(login=username)

            if user.password == password:
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role.role_name
                request.session['user_role_id'] = user.role_id
                request.session['user_full_name'] = user.full_name

                if user.role_id == 1:
                    return redirect('admin_page')
                elif user.role_id == 2:
                    return redirect('manager_page')
                elif user.role_id == 3:
                    return redirect('client_page')
                else:
                    return redirect('guest_page')
            else:
                return render(request, 'aut.html', {'error': 'Неверный пароль'})
        except User.DoesNotExist:
            return render(request, 'aut.html', {'error': 'Пользователь не найден'})
    return render(request, 'aut.html')


def admin_page(request):

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')


    # Базовый запрос всех товаров
    products = Product.objects.all().select_related('category', 'producer', 'provider').order_by('id')

    if sort_by == 'stock_asc':
        products = products.order_by('stock_quantity')
    elif sort_by == 'stock_desc':
        products = products.order_by('-stock_quantity')
    else:
        products = products.order_by('id')

    if query:
        products = products.filter(
            Q(article__icontains=query) |
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(producer__producer_name__icontains=query) |
            Q(provider__provider_name__icontains=query)
        )


    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price

    context = {
        'products': products,
        'query': query,  # передаем поисковый запрос в шаблон
    }
    return render(request, 'admin.html', context)


def manager_page(request):

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')

    products = Product.objects.all().select_related('category', 'producer', 'provider').order_by('id')

    if sort_by == 'stock_asc':
        products = products.order_by('stock_quantity')
    elif sort_by == 'stock_desc':
        products = products.order_by('-stock_quantity')
    else:
        products = products.order_by('id')

    # Если есть поисковый запрос, фильтруем товары
    if query:
        products = products.filter(
            Q(article__icontains=query) |
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(producer__producer_name__icontains=query) |
            Q(provider__provider_name__icontains=query)
        )



    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'manager.html', context)

def client_page(request):
    products = Product.objects.all().order_by('id')
    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price
    return render(request, 'client.html', {'products': products})


def guest_page(request):
    products = Product.objects.all().order_by('id')
    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price
    return render(request, 'guest.html', {'products': products})

def logout_user(request):
    logout(request)
    return redirect('home')