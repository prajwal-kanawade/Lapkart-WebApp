from django.contrib import admin

from .models import Category, Laptop, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ("company", "variant", "category", "price", "stock", "is_featured", "created_at")
    list_filter = ("category", "company", "is_featured")
    search_fields = ("company", "variant", "processor")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("laptop", "user", "rating", "created_at")
    list_filter = ("rating",)
