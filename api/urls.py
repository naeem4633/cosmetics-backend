from django.urls import path, include
from .views import product_list, product_detail, saveditem_list, saveditem_detail, saveditem_create, saveditem_delete, cart_items, wishlist_items, login, register, logout, product_create, saveditem_create
from . import views

urlpatterns = [
    path('products', product_list, name='product-list'),
    path('brand-products/<str:brand_name>', views.brand_products, name='brand_products'),
    path('category-products/<str:category_name>', views.category_products, name='category_products'),
    path('products/create', product_create, name='product-create'),
    path('products/<int:pk>', product_detail, name='product-detail'),
    path('saveditems', saveditem_list, name='saveditem-list'),
    path('saveditems/<int:pk>', saveditem_detail, name='saveditem-detail'),
    path('saveditems/create', saveditem_create, name='saveditem-create'),
    path('saveditems/<int:pk>/delete', saveditem_delete, name='saveditem-delete'),
    path('cart_items', cart_items, name='cart-items'),
    path('wishlist_items', wishlist_items, name='wishlist-items'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
]