from django.urls import path
from . import views
urlpatterns=[
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('register/',views.register_view, name='register'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/users/<int:pk>/toggle-staff/', views.toggle_staff, name='toggle_staff'),
]
