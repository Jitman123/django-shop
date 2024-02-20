from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)

    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(sessions_key=request.session.session_key)