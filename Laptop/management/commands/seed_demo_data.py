from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from Laptop.models import Category, Laptop, Review

DEMO_USERS = [
    {"username": "demo_staff", "password": "DemoStaff123!", "email": "demo_staff@example.com", "is_staff": True},
    {"username": "demo_customer", "password": "DemoCustomer123!", "email": "demo_customer@example.com", "is_staff": False},
]

DEMO_CATEGORIES = ["Everyday & Business", "Gaming", "Ultrabook", "Budget"]

DEMO_LAPTOPS = [
    {
        "company": "Dell", "variant": "Inspiron 15", "processor": "Intel Core i5-1235U",
        "ram": 16, "rom": 512, "category": "Everyday & Business", "price": 54999,
        "stock": 20, "is_featured": True,
        "description": "A reliable all-rounder for work and study, with a crisp 15.6-inch display and all-day battery life.",
    },
    {
        "company": "ASUS", "variant": "ROG Strix G15", "processor": "AMD Ryzen 7 6800H",
        "ram": 16, "rom": 1024, "category": "Gaming", "price": 94999,
        "stock": 10, "is_featured": True,
        "description": "High-refresh-rate gaming laptop with a dedicated RTX GPU for smooth 1080p and 1440p gaming.",
    },
    {
        "company": "Apple", "variant": "MacBook Air M2", "processor": "Apple M2",
        "ram": 8, "rom": 256, "category": "Ultrabook", "price": 114900,
        "stock": 15, "is_featured": True,
        "description": "Fanless, ultra-portable, and built on Apple Silicon for excellent battery life.",
    },
    {
        "company": "HP", "variant": "15s", "processor": "Intel Core i3-1215U",
        "ram": 8, "rom": 512, "category": "Budget", "price": 32999,
        "stock": 30, "is_featured": False,
        "description": "An affordable everyday laptop for browsing, office work, and streaming.",
    },
    {
        "company": "Lenovo", "variant": "Legion 5 Pro", "processor": "Intel Core i7-13700H",
        "ram": 32, "rom": 1024, "category": "Gaming", "price": 134999,
        "stock": 6, "is_featured": False,
        "description": "A high-refresh QHD gaming powerhouse with excellent thermals for sustained performance.",
    },
    {
        "company": "ASUS", "variant": "ZenBook 14 OLED", "processor": "Intel Core i7-1355U",
        "ram": 16, "rom": 512, "category": "Ultrabook", "price": 79999,
        "stock": 12, "is_featured": False,
        "description": "A slim OLED ultrabook ideal for creative work and productivity on the go.",
    },
]


class Command(BaseCommand):
    help = "Seeds the database with fake demo users, categories, and laptop products (safe to run on a fresh clone)."

    def handle(self, *args, **options):
        categories = {}
        for name in DEMO_CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category
        self.stdout.write(self.style.SUCCESS(f"Categories ready ({len(categories)})."))

        for user_data in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"], "is_staff": user_data["is_staff"]},
            )
            if created:
                user.set_password(user_data["password"])
                user.is_staff = user_data["is_staff"]
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user '{user.username}' (password: {user_data['password']})."))
            else:
                self.stdout.write(f"User '{user.username}' already exists, skipping.")

        for lap_data in DEMO_LAPTOPS:
            laptop, created = Laptop.objects.get_or_create(
                company=lap_data["company"],
                variant=lap_data["variant"],
                defaults={
                    "processor": lap_data["processor"],
                    "ram": lap_data["ram"],
                    "rom": lap_data["rom"],
                    "category": categories[lap_data["category"]],
                    "price": lap_data["price"],
                    "stock": lap_data["stock"],
                    "is_featured": lap_data["is_featured"],
                    "description": lap_data["description"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created laptop '{laptop.display_name}'."))
            else:
                self.stdout.write(f"Laptop '{laptop.display_name}' already exists, skipping.")

        demo_customer = User.objects.filter(username="demo_customer").first()
        first_laptop = Laptop.objects.filter(company="Dell", variant="Inspiron 15").first()
        if demo_customer and first_laptop:
            Review.objects.get_or_create(
                laptop=first_laptop,
                user=demo_customer,
                defaults={"rating": 5, "comment": "Great everyday laptop, fast enough for work and light gaming."},
            )

        self.stdout.write(self.style.SUCCESS("\nDemo data ready. Log in with demo_staff / DemoStaff123! or demo_customer / DemoCustomer123!"))
