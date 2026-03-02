from django.urls import path
from obu import views

urlpatterns = [
    path('', views.login_user, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('client/', views.client_page, name='client_page'),
    path('guest/', views.guest_page, name='guest_page'),
    path('admin/', views.admin_page, name='admin_page'),
    path('manager/', views.manager_page, name='manager_page'),

    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete')
]

