from django.urls import path

from . import views

urlpatterns = [
    path('show/', views.show_laptop, name='shop'),
    path('detail/<int:pk>/', views.laptop_detail, name='laptop_detail'),
    path('review/add/<int:pk>/', views.add_review, name='add_review'),
    path('manage/', views.manage_products, name='manage_products'),
    path('add/', views.add_laptop, name='add_laptop'),
    path('update/<int:i>/', views.update_laptop, name='update_laptop'),
    path('delete/<int:i>/', views.delete_laptop, name='delete_laptop'),
]
