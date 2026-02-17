from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import User, Product

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
    products = Product.objects.all().order_by('id')
    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price
    return render(request, 'admin.html', {'products': products})

def manager_page(request):
    products = Product.objects.all().order_by('id')
    for prod in products:
        if prod.discount_percent > 0:
            prod.discounted_price = prod.price * (1 - prod.discount_percent / 100)
        else:
            prod.discounted_price = prod.price
    return render(request, 'manager.html', {'products': products})

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