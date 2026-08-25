from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from Laptop.decorators import staff_required
from Laptop.models import Laptop

from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem, Wishlist


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("laptop")
    total = sum(item.subtotal for item in items)
    context = {"items": items, "total": total}
    return render(request, "Orders/cart.html", context)


@login_required
def add_to_cart(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, laptop=laptop)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{laptop.display_name} added to cart.")
    return redirect(request.META.get("HTTP_REFERER", "cart"))


@login_required
def update_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1
        if quantity < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
    return redirect("cart")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user).select_related("laptop")
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    total = sum(item.subtotal for item in items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            for item in items:
                if item.quantity > item.laptop.stock:
                    messages.error(request, f"Not enough stock for {item.laptop.display_name}.")
                    return redirect("cart")

            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total
                order.save()
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        laptop=item.laptop,
                        product_label=item.laptop.display_name,
                        price=item.laptop.price,
                        quantity=item.quantity,
                    )
                    Laptop.objects.filter(pk=item.laptop.pk).update(stock=F("stock") - item.quantity)
                items.delete()
            return redirect("order_confirmation", order_id=order.id)
    else:
        form = CheckoutForm()

    context = {"form": form, "items": items, "total": total}
    return render(request, "Orders/checkout.html", context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "Orders/order_confirmation.html", {"order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "Orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, pk=order_id)
    else:
        order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "Orders/order_detail.html", {"order": order})


@staff_required
def manage_orders(request):
    orders = Order.objects.select_related("user").all()
    status_filter = request.GET.get("status")
    if status_filter:
        orders = orders.filter(status=status_filter)
    context = {"orders": orders, "status_choices": Order.STATUS_CHOICES, "status_filter": status_filter}
    return render(request, "Orders/manage_orders.html", context)


@staff_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} marked as {order.get_status_display()}.")
    return redirect("manage_orders")


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("laptop")
    return render(request, "Orders/wishlist.html", {"items": items})


@login_required
def toggle_wishlist(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    item, created = Wishlist.objects.get_or_create(user=request.user, laptop=laptop)
    if not created:
        item.delete()
        messages.info(request, f"{laptop.display_name} removed from wishlist.")
    else:
        messages.success(request, f"{laptop.display_name} added to wishlist.")
    return redirect(request.META.get("HTTP_REFERER", "wishlist"))
