from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


# Create your views here.
def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
    else:
        carts = Cart.objects.filter(sessions_key=request.session.session_key, product=product)

    if carts.exists():
        cart = carts.first()
        if cart:
            cart.quantity += 1
            cart.save()
    else:
        if request.user.is_authenticated:
            Cart.objects.create(user=request.user, product=product, quantity=1)
        else:
            Cart.objects.create(sessions_key=request.session.session_key, product=product, quantity=1)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': get_user_carts(request)}, request=request
    )

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html
    }

    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')
    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': get_user_carts(request)}, request=request
    )
    response_data = {
        'message': 'Количество изменено',
        'cart_items_html': cart_items_html,
        'quantity': updated_quantity
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': get_user_carts(request)}, request=request
    )

    response_data = {
        'message': 'Товар удален',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity
    }

    return JsonResponse(response_data)
