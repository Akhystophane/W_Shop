import uuid

from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from accounts.models import Shopper, FormShopper
from store.models import Product, Cart, Order
User = get_user_model()
def get_user(request):
    device = request.COOKIES['device']
    user = request.user
    try:
        value = user.is_registered

    except:
        user, user_created = User.objects.get_or_create(device=device, username=device)

    return user

# Create your views here.
def index(request):
    products = Product.objects.all()
    try:
        user = get_user(request)
    except:
        return render(request, 'store/index.html', context={"products": products})

    return render(request, 'store/index.html', context={"products": products, "user":user})

def best_seller(request):
    products = Product.objects.all()
    try:
        user = get_user(request)
    except:
        return render(request, 'store/best_seller.html', context={"products": products})

    return render(request, 'store/best_seller.html', context={"products": products, "user":user})

def featured(request):
    products = Product.objects.all()
    try:
        user = get_user(request)
    except:
        return render(request, 'store/featured.html', context={"products": products})

    return render(request, 'store/featured.html', context={"products": products, "user":user})

def new_arrival(request):
    products = Product.objects.all()
    try:
        user = get_user(request)
    except:
        return render(request, 'store/new_arrival.html', context={"products": products})

    return render(request, 'store/new_arrival.html', context={"products": products, "user":user})


def product_detail(request, slug):
    user = get_user(request)
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/details.html', context={"product": product, "user":user})


def add_to_cart(request, slug):
    user = get_user(request)
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)

    if created:
        cart.orders.add(order)
        order.cost = order.product.price
        order.save()
        cart.save()
    else:
        order.quantity += 1
        order.cost = order.product.price * order.quantity
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))

def del_product(request, slug):
    user = get_user(request)
    _product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user, )
    order, created = Order.objects.get_or_create(user=user, product=_product, ordered=False)
    order.delete()
    return redirect(reverse('cart'))

def increment_cart(request, slug):
    user = get_user(request)
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user, )
    order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)
    order.quantity += 1
    order.cost = order.product.price * order.quantity
    order.save()
    return redirect(reverse('cart'))

def decrement_cart(request, slug):
    user = get_user(request)
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user, )
    order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)
    order.quantity -= 1
    if order.quantity <= 0:
        order.delete()
        return redirect(reverse('cart'))
    order.cost = order.product.price * order.quantity
    order.save()
    return redirect(reverse('cart'))

# def payment(request):
#     user = get_user(request)
#     cart


def cart(request):
    user = get_user(request)
    cart,_ = Cart.objects.get_or_create(user=user)
    total = Order.objects.filter(ordered=False, user=user).aggregate(Sum("cost"))
    total_items = Order.objects.filter(ordered=False, user=user).annotate(Sum("product")).count()
    if total['cost__sum'] == None:
        total['cost__sum'] = 0

    return render(request, 'store/cart.html', context={"orders": cart.orders.all, "total":total, "total_items":total_items, "user":user})


def delete_cart(request):
    user = get_user(request)
    if cart := user.cart:
        cart.delete()
    return redirect('index')

def checkout(request):
    user = get_user(request)

    cart = get_object_or_404(Cart, user=user)
    shopper = get_object_or_404(Shopper, username=user.username)
    total = Order.objects.filter(ordered=False, user=user).aggregate(Sum("cost"))
    total_items = Order.objects.filter(ordered=False, user=user).annotate(Sum("product")).count()

    if request.method == "POST":
        if not request.user.is_authenticated:
            last_name = request.POST.get("last_name")
            first_name = request.POST.get("first_name")
            email = request.POST.get("email")
            shopper.last_name = last_name
            shopper.first_name = first_name
            shopper.email = email

        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")
        state = request.POST.get("state")
        city = request.POST.get("city")
        shopper.address = address
        shopper.zipcode = zipcode
        shopper.state = state
        shopper.city = city
        shopper.save()
        return redirect('index')
    # return render(request, 'accounts/signup.html')

            # shopper.address = form.cleaned_data.get('form_address')
            # shopper.state = form.cleaned_data.get('form_state')
            # shopper.zipcode = form.cleaned_data.get('form_zipcode')
            # shopper.city = form.cleaned_data.get('form_city')
            # shopper.save()

    # else:
    #     form = FormShopper()



    # shopper.address = request.POST.get("address")
    # shopper.state = request.POST.get("state")
    # shopper.zipcode = request.POST.get("zipcode")
    # shopper.city = request.POST.get("city")
    # shopper.save()

    return render(request, 'store/checkout.html', context={"user":user, "orders": cart.orders.all, "shoppers": shopper, "total":total, "total_items":total_items})

def payment(request):
    user = get_user(request)
    cart = get_object_or_404(Cart, user=user)
    shopper = get_object_or_404(Shopper, username=user.username)
    total = Order.objects.filter(ordered=False, user=user).aggregate(Sum("cost"))
    total_items = Order.objects.filter(ordered=False, user=user).annotate(Sum("product")).count()

    return render(request, 'store/payment.html', context={"user":user, "orders": cart.orders.all, "shoppers": shopper,
                                                           "total":total, "total_items":total_items})