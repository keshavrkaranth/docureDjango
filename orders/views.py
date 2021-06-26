from django.shortcuts import redirect, render
from django.http import HttpResponse
from cart.models import CartItem, Cart
from .models import Order
import datetime
from .constants import client, key
from django.views.decorators.csrf import csrf_exempt

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

        print(response)
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


@csrf_exempt
def razorpay_payment(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("Done payment hurrey!")
