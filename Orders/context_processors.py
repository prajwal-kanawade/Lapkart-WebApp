from .models import CartItem, Wishlist


def cart_context(request):
    if request.user.is_authenticated:
        cart_count = sum(
            CartItem.objects.filter(user=request.user).values_list("quantity", flat=True)
        )
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        cart_count = 0
        wishlist_count = 0
    return {"cart_count": cart_count, "wishlist_count": wishlist_count}
