from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import staff_required
from .forms import LaptopModelForm, ReviewForm
from .models import Category, Laptop, Review


def home(request):
    featured = Laptop.objects.filter(is_featured=True)[:6]
    if not featured:
        featured = Laptop.objects.all()[:6]
    categories = Category.objects.all()
    context = {"featured": featured, "categories": categories}
    return render(request, "Laptop/home.html", context)


def show_laptop(request):
    lap = Laptop.objects.select_related("category").all()

    query = request.GET.get("q", "").strip()
    if query:
        lap = lap.filter(
            Q(company__icontains=query) | Q(variant__icontains=query) | Q(processor__icontains=query)
        )

    category_id = request.GET.get("category")
    if category_id:
        lap = lap.filter(category_id=category_id)

    min_price = request.GET.get("min_price")
    if min_price:
        lap = lap.filter(price__gte=min_price)

    max_price = request.GET.get("max_price")
    if max_price:
        lap = lap.filter(price__lte=max_price)

    sort = request.GET.get("sort", "newest")
    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
    }
    lap = lap.order_by(sort_map.get(sort, "-created_at"))

    paginator = Paginator(lap, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category_id,
        "sort": sort,
        "min_price": min_price or "",
        "max_price": max_price or "",
    }
    return render(request, "Laptop/show_laptop.html", context)


def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop.objects.select_related("category"), pk=pk)
    reviews = laptop.reviews.select_related("user").all()
    related = Laptop.objects.filter(category=laptop.category).exclude(pk=laptop.pk)[:4]

    user_review = None
    review_form = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    context = {
        "laptop": laptop,
        "reviews": reviews,
        "related": related,
        "user_review": user_review,
        "review_form": review_form,
    }
    return render(request, "Laptop/laptop_detail.html", context)


@login_required
def add_review(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    if request.method == "POST" and not laptop.reviews.filter(user=request.user).exists():
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.laptop = laptop
            review.user = request.user
            review.save()
            messages.success(request, "Thanks for your review!")
    return redirect("laptop_detail", pk=pk)


@staff_required
def manage_products(request):
    lap = Laptop.objects.select_related("category").all()
    return render(request, "Laptop/manage_products.html", {"lap": lap})


@staff_required
def add_laptop(request):
    form = LaptopModelForm()
    if request.method == "POST":
        form = LaptopModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Laptop added successfully.")
            return redirect("manage_products")

    context = {"form": form, "title": "Add New Laptop"}
    return render(request, "Laptop/add_laptop.html", context)


@staff_required
def update_laptop(request, i):
    lap_obj = get_object_or_404(Laptop, pk=i)
    form = LaptopModelForm(instance=lap_obj)
    if request.method == "POST":
        form = LaptopModelForm(request.POST, request.FILES, instance=lap_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Laptop updated successfully.")
            return redirect("manage_products")

    context = {"form": form, "title": f"Edit {lap_obj.display_name}"}
    return render(request, "Laptop/add_laptop.html", context)


@staff_required
def delete_laptop(request, i):
    lap_obj = get_object_or_404(Laptop, pk=i)
    if request.method == "POST":
        lap_obj.delete()
        messages.info(request, "Laptop deleted.")
        return redirect("manage_products")
    return render(request, "Laptop/delete_confirm.html", {"laptop": lap_obj})
