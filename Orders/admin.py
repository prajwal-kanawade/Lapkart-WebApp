from django.contrib import admin

from .models import CartItem, Order, OrderItem, Wishlist


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "total_amount", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("user__username", "full_name", "phone")
    inlines = [OrderItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "laptop", "quantity", "added_at")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "laptop", "added_at")
