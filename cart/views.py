from django.shortcuts import render, redirect, get_object_or_404
from store.models import Products
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user

    product = Products.objects.get(id=product_id)

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cartId=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cartId=_cart_id(request))
            cart.save()
        try:
            print("try")
            cart_item = CartItem.objects.get(
                product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            print("in except")
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1,
                cart=cart
            )
        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cartId=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cartId=_cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
        return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    shipping_cost = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cartId=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        shipping_cost = total//20
        grand_total = total+tax+shipping_cost
    except:
        pass

    data = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }

    return render(request, 'cart/cart.html', data)


def sub_product(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Products, id=product_id)
        cart_item = CartItem.objects.get(user=current_user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')

    else:
        cart = Cart.objects.get(cartId=_cart_id(request))
        product = get_object_or_404(Products, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')


def remove_from_cart(request, product_id):
    current_user = request.user

    if current_user.is_authenticated:
        product = get_object_or_404(Products, id=product_id)
        cart_item = CartItem.objects.filter(
            user=current_user, product=product).delete()
        return redirect('cart')

    else:
        cart = Cart.objects.get(cartId=_cart_id(request))
        product = get_object_or_404(Products, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    current_user = request.user
    cart_items_count = CartItem.objects.filter(user=current_user).count()
    if cart_items_count <= 0:
        return redirect('products')

    total = 0
    tax = 0
    quantity = 0

    if current_user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(
                user=current_user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            shipping_cost = total//20
            grand_total = total+tax+shipping_cost
        except:
            pass

    else:
        try:
            cart = Cart.objects.get(cartId=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            shipping_cost = total//20
            grand_total = total+tax+shipping_cost
        except:
            pass

    data = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }
    return render(request, 'checkout/checkout.html', data)
