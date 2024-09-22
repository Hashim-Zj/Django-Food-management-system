from Users.models import Wishlist, Cart

def index_count(request):
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user, status="in-cart").count()
    else:
        wishlist_count = 0
        cart_count = 0

    return {
        "wishlist_count": wishlist_count,
        "cart_count": cart_count,
    }
