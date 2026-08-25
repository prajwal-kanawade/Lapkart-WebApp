from django.db import migrations


CATEGORY_NAMES = ["Everyday & Business", "Gaming", "Ultrabook", "Budget"]

# (company, variant) -> (category_name, price, stock, is_featured)
OVERRIDES = {
    ("Lenovo", "Ideapad"): ("Everyday & Business", 42999, 18, True),
    ("Acer", "Black"): ("Budget", 34999, 25, False),
    ("Lenovo", "Idepad"): ("Everyday & Business", 52999, 12, True),
    ("Apple", "Mackbook"): ("Ultrabook", 129999, 8, False),
}


def backfill(apps, schema_editor):
    Category = apps.get_model("Laptop", "Category")
    Laptop = apps.get_model("Laptop", "Laptop")

    categories = {name: Category.objects.get_or_create(name=name)[0] for name in CATEGORY_NAMES}

    for laptop in Laptop.objects.all():
        key = (laptop.company, laptop.variant)
        category_name, price, stock, featured = OVERRIDES.get(
            key, ("Everyday & Business", 39999, 10, False)
        )
        laptop.category = categories[category_name]
        laptop.price = price
        laptop.stock = stock
        laptop.is_featured = featured
        laptop.description = (
            f"{laptop.company} {laptop.variant} laptop featuring {laptop.processor}, "
            f"{laptop.ram}GB RAM and {laptop.rom:g}GB storage. A dependable choice for "
            f"work, study, and everyday computing."
        )
        laptop.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("Laptop", "0003_category_alter_laptop_options_laptop_created_at_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill, noop),
    ]
