from django.shortcuts import render,get_object_or_404
from .forms import ProductFilter

from category.models import Category
from .models import Products
from cart.models import CartItem
from cart.views import _cart_id

# Create your views here.
def products(request,category_slug=None):
    product=None
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        product = Products.objects.filter(category=categories,is_avilable=True)
        product_count = product.count()
    else:
        categories = Category.objects.all()
        product = Products.objects.all().filter(is_avilable=True,)
        product_count = product.count()

    data = {
        'product':product,
        'product_count':product_count

    }

    return render(request, 'product/products.html',data)


def product_description(request,catogery_slug,product_slug):
    try:
        single_product = Products.objects.get(category__slug=catogery_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cartId=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    data = {
        'single_product':single_product,
        'in_cart':in_cart
    }
    return render(request,'product/product_description.html',data)

def product_list(request):
    filter = ProductFilter(request.GET, queryset=Products.objects.all())
    return render(request, 'test.html', {'filter': filter})
