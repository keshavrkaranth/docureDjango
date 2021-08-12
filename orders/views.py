from django.shortcuts import redirect, render
from django.http import HttpResponse
from cart.models import CartItem, Cart
from .models import Order, Payment, OrderProduct
import datetime
from .constants import client, key
from django.views.decorators.csrf import csrf_exempt
from store.models import Products

# Create your views here.


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(
        user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('products')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    shipping_cost = total//20
    grand_total = total+tax+shipping_cost
    if request.method == 'POST':
        data = Order()
        data.user = current_user
        data.first_name = request.POST.get('fname')
        data.last_name = request.POST.get('lname')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.address_line_1 = request.POST.get('ad1')
        data.address_line_2 = request.POST.get('ad2')
        data.country = request.POST.get('country')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.pincode = request.POST.get('pincode')
        data.order_note = request.POST.get('shipping')
        data.total = total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date+str(data.id)
        data.order_number = order_number
        data.save()
        order_data = Order.objects.get(
            user=current_user, order_number=order_number, is_ordered=False)
        order_amount = int(grand_total) * 100
        response = client.order.create(
            {'amount': order_amount, 'currency': 'INR', 'receipt': order_number, 'payment_capture': 1})

        data = {
            'key': key,
            'order': order_data,
            'total': total,
            'tax': tax,
            'shipping_cost': shipping_cost,
            'grand_total': grand_total,
            'cart_items': cart_items,
            'response': response,
        }
        return render(request, 'orders/payments.html', data)
    else:
        return redirect('checkout')


# <QueryDict: {'hidden': [''], 'razorpay_payment_id': ['pay_HRzpX1vf4QeunS'], 'razorpay_order_id': ['order_HRzp3oa8UfsG72'], 'razorpay_signature': ['675bf37cc35f987d0f47a927036b649481144e6023d59534d0dcca240166543b'], 'org_logo': [''], 'org_name': ['Razorpay Software Private Ltd'], 'checkout_logo': ['https://cdn.razorpay.com/logo.png'], 'custom_branding': ['false']} >

@csrf_exempt
def razorpay_payment(request, order_no, total=0, quantity=0):
    if request.method == "POST":
        data = request.POST
        print(order_no)
        order_data = Order.objects.get(
            user=request.user, order_number=order_no, is_ordered=False)
        payment = Payment.objects.create(user=request.user, payment_id=data.get(
            'razorpay_payment_id'), payment_method='Razorpay', amount_paid=order_data.total)
        payment.save()
        order_data.payment = payment
        order_data.is_ordered = True
        order_data.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order_data.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.is_ordered = True
            order_product.save()

            product = Products.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        data = {
            'cart_items': cart_items,
            'total': total,
            'quantity': quantity,
            'order_no': order_no,
        }

        return render(request, 'orders/success.html', data)


def test(request):
    return render(request, 'orders/success.html')
