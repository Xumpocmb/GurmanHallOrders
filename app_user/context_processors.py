from app_user.models import CartItem


def carts(request):
    return {'user_carts': CartItem.objects.filter(user=request.user) if request.user.is_authenticated else []}
