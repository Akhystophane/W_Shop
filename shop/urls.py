"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_cart, increment_cart, decrement_cart, checkout, \
    payment, best_seller, featured, new_arrival, del_product
from shop import settings
from accounts.views import signup, logout_user, login_user

urlpatterns = [
    path('', index, name='index'),
    path('best_seller', best_seller, name='best_seller'),
    path('featured', featured, name='featured'),
    path('new_arrival', new_arrival, name='new_arrival'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/payment', payment, name='payment'),
    path('cart/del_product/<str:slug>', del_product, name='del_product'),
    path('cart/increment/<str:slug>', increment_cart, name='increment_cart'),
    path('cart/decrement/<str:slug>', decrement_cart, name='decrement_cart'),
    path('cart/delete/', delete_cart, name='delete-cart'),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart', add_to_cart, name="add-to-cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
