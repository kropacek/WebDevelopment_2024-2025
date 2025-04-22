from django.urls import path

from .views import product_list, product_detail, about_view

app_name = 'shop_app'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('about/', about_view, name='about'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
]