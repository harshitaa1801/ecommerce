from datetime import datetime
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,F, ExpressionWrapper, DecimalField
from ecomm.custom_decorator import ajax_login_required
import razorpay


from .models import Address, Cart, Cart_Item, Order, Product

from ecomm import settings

# Create your views here.

RAZORPAY_CLIENT = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))

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


@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        return JsonResponse({'message': 'Please add items to the cart'})
    cart_items = Cart_Item.objects.filter(cart=cart).annotate(
        total_price=ExpressionWrapper(
            F('quantity') * F('product__price'),
            output_field=DecimalField()
        )
    )
    total = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    cart_item_count = cart_items.count()
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total, 'cart_id': cart.id, 'cart_item_count': cart_item_count})



@login_required
def remove_from_cart(request, cart_item_id):
    cart = Cart.objects.get(user=request.user)
    Cart_Item.objects.filter(id=cart_item_id, cart=cart).delete()
    return redirect('view_cart')


@login_required
def update_cart(request, cart_item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(Cart_Item, id=cart_item_id, cart=cart)
    action = request.GET.get('action')

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return JsonResponse({'deleted': True})

    cart_item.save()
    return JsonResponse({
        'quantity': cart_item.quantity,
        'total': cart_item.quantity*cart_item.product.price,
        'cart_total': Cart_Item.objects.filter(cart=cart).aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    })


@login_required
def place_order(request):
    if request.method == 'GET':
        user=request.user
        cart_id = request.GET.get('cart_id')
        total_price = Cart_Item.objects.filter(cart_id=cart_id).aggregate(total=Sum(F('quantity') * F('product__price')))['total']
        address = Address.objects.filter(user=user).order_by('-id').first()
        return render(request, 'shop/order_form.html', {'total_price': total_price, 'cart_id': cart_id, 'address': address})

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        amount = float(request.POST.get('total_price')) * 100  # Convert to paisa
        cart_id = request.POST.get('cart_id')
        user=request.user

        address = Address.objects.create(
            user = user,
            name = name,
            email = email,
            phone = phone,
            street_address=street_address,
            city=city,
            state = state,
            zip_code = zip_code,
            country = country
        )

        order = Order.objects.create(
            address=address,
            total_price=amount / 100,
            cart_id=cart_id,
            user=user
        )

        cart_items = Cart_Item.objects.filter(cart_id = cart_id)
        order.items.set(cart_items)

        razorpay_order = RAZORPAY_CLIENT.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })
        
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        return render(request, 'shop/payment.html', {'order': order, 'razorpay_order': razorpay_order})
    

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        
        order = Order.objects.get(razorpay_order_id=order_id)
        order.payment_status = 'PAID'
        order.razorpay_payment_id = payment_id
        order.updated_at = datetime.now()
        order.save()

        # removing those items from cart
        Cart_Item.objects.filter(cart=order.cart).delete()
        
        return render(request, 'shop/payment_success.html', {'order': order})

    return redirect('ShopHome')