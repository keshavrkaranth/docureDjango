from django.shortcuts import render, get_object_or_404
from category.models import Category
from store.models import Products

# Create your views here.


def homePage(request):
    cat = Category.objects.all()
    data = {
        'category': cat,

    }

    return render(request, 'index1.html', data)


def missions(request):
    return render(request, 'mission.html')


def about(request):
    return render(request, 'about.html')


def category_product_description(request, catogery_slug, product_slug):
    try:
        single_product = Products.objects.get(
            category__slug=catogery_slug, slug=product_slug)
    except Exception as e:
        raise e

    data = {
        'single_product': single_product,
    }
    return render(request, 'category_product_description.html', data)
