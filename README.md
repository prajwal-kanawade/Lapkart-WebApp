# LapKart

A full-featured ecommerce web application for laptops — product catalog, cart, checkout, order tracking, reviews, wishlists, and a staff management dashboard — built with Django.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.1-092E20?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-dev%20db-003B57?logo=sqlite&logoColor=white)

## Features

**Storefront**
- Public product catalog with search, category/price filters, sorting, and pagination
- Product detail pages with specs, stock status, related products, and star-rated reviews
- Cart with quantity updates and live item count in the navbar
- Wishlist
- Checkout with shipping details and mock payment (Cash on Delivery / Card)
- Order history and order detail pages for customers

**Accounts & roles**
- Registration and login with session-based auth
- Two-tier access model: regular customers vs. staff
- Staff-only management dashboard to add/edit/delete products (with image upload) and update order statuses
- **Manage Users** page — staff can grant or revoke staff access on other accounts, with safeguards: you can't change your own status, and only a superuser can change another superuser's access

**Engineering**
- Secrets (Django secret key, debug flag, allowed hosts) loaded from a gitignored `.env` file, never hardcoded
- Seed command for realistic demo data on a fresh clone, without touching real user data
- Data migration that safely backfilled the original product records when the schema was extended

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Django 5.1.1 |
| Database | SQLite (dev) |
| Frontend | Django Templates, Bootstrap 5, Bootstrap Icons |
| Image handling | Pillow |
| Auth | Django's built-in auth system (`django.contrib.auth`) |

## Project Structure

```
LapKart/
├── LapKart/            # project settings, root URLconf
├── AuthApp/             # login, registration, user/role management
├── Laptop/               # product catalog: categories, products, reviews, staff CRUD
│   └── management/commands/seed_demo_data.py
├── Orders/              # cart, wishlist, checkout, orders
├── templates/            # Django templates, organized per app
├── static/               # CSS, images
├── media/                # uploaded product images (gitignored)
├── requirements.txt
└── manage.py
```

## Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
git clone https://github.com/prajwal-kanawade/Lapkart-WebApp.git
cd Lapkart-WebApp
pip install -r requirements.txt
```

### Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` and set a real `DJANGO_SECRET_KEY` (generate one with the command below):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django cryptographic signing key | dev-only fallback (not safe for production) |
| `DJANGO_DEBUG` | Enables debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames | `*` |

### Set up the database

```bash
python manage.py migrate
python manage.py seed_demo_data   # optional: populate fake demo users/products
```

### Run the server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**.

## Demo Credentials

If you ran `seed_demo_data`, log in with:

| Role | Username | Password |
|---|---|---|
| Staff | `demo_staff` | `DemoStaff123!` |
| Customer | `demo_customer` | `DemoCustomer123!` |

## Key Routes

| URL | Description |
|---|---|
| `/` | Home page with featured products |
| `/laptop/show/` | Shop — search, filter, sort |
| `/laptop/detail/<id>/` | Product detail + reviews |
| `/orders/cart/` | Cart |
| `/orders/checkout/` | Checkout |
| `/orders/my/` | Order history |
| `/orders/wishlist/` | Wishlist |
| `/auth/login/`, `/auth/register/` | Authentication |
| `/laptop/manage/` | Staff: manage products |
| `/orders/manage/` | Staff: manage orders |
| `/auth/manage/users/` | Staff: manage user roles |

## Roadmap

- [ ] Password reset via email
- [ ] Dedicated seller role with scoped product/order management
- [ ] Customer-initiated order cancellation
- [ ] Coupon / discount codes
- [ ] Automated test suite
- [ ] Production deployment (Postgres, WhiteNoise/S3 for static & media)

## License

No license specified yet — all rights reserved by the author unless stated otherwise.
