from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def index(request):
    category = Product.objects.values('category', 'id')
    category_set = {item['category'] for item in category}

    allprods = []
    for cat in category_set:
        products = Product.objects.filter(category = cat)
        products_count = products.count()

        if products_count % 4 == 0:
            num_of_slides = products_count // 4
        else:
            num_of_slides = products_count // 4 + 1
        allprods.append([products, num_of_slides, range(1, num_of_slides)])

    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact_us(request):
    return render(request, 'shop/contact.html')

def product_view(request, id):
    try:
        product_obj = Product.objects.get(id=id)
        return render(request, 'shop/productView.html', {'product': product_obj})
        # return HttpResponse(f'{product_obj.name}')
    except Product.DoesNotExist:
        return HttpResponse('does not exist')
    # return HttpResponse('This is product page')

def search(request):
    return HttpResponse('This is search page')

def tracker(request):
    return HttpResponse('This is tracker page')

def checkout(request):
    return HttpResponse('This is checkout page')