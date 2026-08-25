from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from Laptop.decorators import staff_required

from .forms import RegisterForm


def login_view(request):
    if request.method == "POST":
        u = request.POST["uname"]
        p = request.POST["pw"]
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    template_name = "AuthApp/login.html"
    context = {"next": request.GET.get("next", "")}
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/auth/login/")


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("/auth/login/")
    template_name = "AuthApp/register.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_required
def manage_users(request):
    users = User.objects.all().order_by("username")
    return render(request, "AuthApp/manage_users.html", {"users": users})


@staff_required
def toggle_staff(request, pk):
    target = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        if target.pk == request.user.pk:
            messages.error(request, "You can't change your own staff status.")
        elif target.is_superuser and not request.user.is_superuser:
            messages.error(request, "Only a superuser can change another superuser's access.")
        else:
            target.is_staff = not target.is_staff
            target.save()
            state = "granted" if target.is_staff else "revoked"
            messages.success(request, f"Staff access {state} for {target.username}.")

    return redirect("manage_users")
