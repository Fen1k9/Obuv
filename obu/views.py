from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import User, Product, Category, Producer, Provider, Unit
from django.db.models import Q
from django.contrib import messages


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
    # Проверка прав доступа (только администратор)
    if request.session.get('user_role_id') != 1:
        return redirect('login')

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')
    provider_filter = request.GET.get('provider', '')

    products = Product.objects.all().select_related('category', 'producer', 'provider', 'unit')

    if provider_filter and provider_filter != 'all':
        products = products.filter(provider_id=provider_filter)

    if query:
        products = products.filter(
            Q(article__icontains=query) |
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(producer__producer_name__icontains=query) |
            Q(provider__provider_name__icontains=query)
        )

    if sort_by == 'stock_asc':
        products = products.order_by('stock_quantity')
    elif sort_by == 'stock_desc':
        products = products.order_by('-stock_quantity')
    else:
        products = products.order_by('id')

    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price

    providers = Provider.objects.all().order_by('provider_name')

    context = {
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'providers': providers,
        'selected_provider': provider_filter,
    }
    return render(request, 'admin.html', context)


def product_add(request):
    """Добавление нового товара"""
    # Проверка прав доступа (только администратор)
    if request.session.get('user_role_id') != 1:
        return redirect('login')

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            article = request.POST.get('article')
            product_name = request.POST.get('product_name')
            category_id = request.POST.get('category')
            producer_id = request.POST.get('producer')
            provider_id = request.POST.get('provider')
            unit_id = request.POST.get('unit')
            price = request.POST.get('price')
            discount_percent = request.POST.get('discount_percent', 0)
            stock_quantity = request.POST.get('stock_quantity', 0)
            description = request.POST.get('description', '')
            photo = request.POST.get('photo', '')

            # Создаем новый товар
            product = Product.objects.create(
                article=article,
                product_name=product_name,
                category_id=category_id,
                producer_id=producer_id,
                provider_id=provider_id,
                unit_id=unit_id,
                price=price,
                discount_percent=discount_percent,
                stock_quantity=stock_quantity,
                description=description,
                photo=photo
            )

            messages.success(request, f'Товар "{product_name}" успешно добавлен')
            return redirect('admin_page')

        except Exception as e:
            messages.error(request, f'Ошибка при добавлении товара: {str(e)}')

    # Получаем данные для выпадающих списков
    categories = Category.objects.all().order_by('category_name')
    producers = Producer.objects.all().order_by('producer_name')
    providers = Provider.objects.all().order_by('provider_name')
    units = Unit.objects.all().order_by('unit_name')

    context = {
        'categories': categories,
        'producers': producers,
        'providers': providers,
        'units': units,
        'is_edit': False
    }
    return render(request, 'product_form.html', context)


def product_edit(request, product_id):
    """Редактирование существующего товара"""
    # Проверка прав доступа (только администратор)
    if request.session.get('user_role_id') != 1:
        return redirect('login')

    # Получаем товар или 404
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # Обновляем данные товара
            product.article = request.POST.get('article')
            product.product_name = request.POST.get('product_name')
            product.category_id = request.POST.get('category')
            product.producer_id = request.POST.get('producer')
            product.provider_id = request.POST.get('provider')
            product.unit_id = request.POST.get('unit')
            product.price = request.POST.get('price')
            product.discount_percent = request.POST.get('discount_percent', 0)
            product.stock_quantity = request.POST.get('stock_quantity', 0)
            product.description = request.POST.get('description', '')
            product.photo = request.POST.get('photo', '')

            product.save()

            messages.success(request, f'Товар "{product.product_name}" успешно обновлен')
            return redirect('admin_page')

        except Exception as e:
            messages.error(request, f'Ошибка при обновлении товара: {str(e)}')

    # Получаем данные для выпадающих списков
    categories = Category.objects.all().order_by('category_name')
    producers = Producer.objects.all().order_by('producer_name')
    providers = Provider.objects.all().order_by('provider_name')
    units = Unit.objects.all().order_by('unit_name')

    context = {
        'product': product,
        'categories': categories,
        'producers': producers,
        'providers': providers,
        'units': units,
        'is_edit': True
    }
    return render(request, 'product_form.html', context)


def product_delete(request, product_id):
    """Удаление товара"""
    # Проверка прав доступа (только администратор)
    if request.session.get('user_role_id') != 1:
        return redirect('login')

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product_name = product.product_name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален')

    return redirect('admin_page')


def manager_page(request):
    # Получаем параметры из GET запроса
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')
    provider_filter = request.GET.get('provider', '')

    # Базовый запрос всех товаров
    products = Product.objects.all().select_related('category', 'producer', 'provider')

    # Применяем фильтр по поставщику
    if provider_filter and provider_filter != 'all':
        products = products.filter(provider_id=provider_filter)

    # Применяем поиск
    if query:
        products = products.filter(
            Q(article__icontains=query) |
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(producer__producer_name__icontains=query) |
            Q(provider__provider_name__icontains=query)
        )

    # Применяем сортировку
    if sort_by == 'stock_asc':
        products = products.order_by('stock_quantity')
    elif sort_by == 'stock_desc':
        products = products.order_by('-stock_quantity')
    else:
        products = products.order_by('id')

    # Рассчитываем цену со скидкой
    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price

    # Получаем всех поставщиков для выпадающего списка
    providers = Provider.objects.all().order_by('provider_name')

    context = {
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'providers': providers,
        'selected_provider': provider_filter,
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