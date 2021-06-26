from cart.models import Cart
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import Signupform
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
import re

# Create your views here.


def signup(request):
    msg = ''
    form = Signupform()
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username = email.split('@')[0]
            if password != confirm_password:
                messages.error(request, 'Two password should be same!')
            else:
                user = Account.objects.create_user(
                    name=name, username=username, email=email, password=password)
                user.phone_number = phone_number
                user.is_active = True
                user.save()
                messages.success(request, 'Registration Successful')
                return redirect('login')
        else:
            form = Signupform()

    data = {
        'form': Signupform(),
        'msg': msg,
    }
    return render(request, 'accounts/signup.html', data)


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cartId=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                parms = dict(x.split('=') for x in query.split('&'))
                if 'next' in parms:
                    nextpage = parms['next']
                    return redirect(nextpage)
            except:
                return redirect('homepage')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('homepage')
