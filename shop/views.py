from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required

from ecomm.custom_decorator import ajax_login_required


from .models import Cart, Cart_Item, Product
# Create your views here.


def index(request):
    user_agent = get_user_agent(request)
    is_mobile = user_agent.is_mobile

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

        if is_mobile:
            if products_count % 2 == 0:
                num_of_slides = products_count // 2
            else:
                num_of_slides = products_count // 2 + 1
        
        # num_of_cards = 2 if is_mobile else 4

        
            
        allprods.append([products, num_of_slides, range(1, num_of_slides)])

    params = {'allprods': allprods, 'is_mobile': is_mobile,}
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

@ajax_login_required
def add_to_cart(request, id):
    print('request: ', request)
    print(request.user)
    print(id)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'message': "This product does not exist"})
    
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)


    item_set = Cart_Item.objects.filter(cart=cart, product = product)

    if item_set.exists():
        item = item_set.first()
        item.quantity += 1
        item.save()
    
    else:
        Cart_Item.objects.create(cart=cart, product = product, quantity=1)

    return JsonResponse({'message':f'You are adding product id {id} to cart'})