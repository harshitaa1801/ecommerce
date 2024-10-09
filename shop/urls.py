from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('about/', views.about, name='AboutUs'),
    # path('contact-us/', views.contact_us, name='ContactUs'),
    path('products/<int:id>/', views.product_view, name='Products'),
    path('search/', views.search, name='Search'),
    path('tracker/', views.tracker, name='Tracker'),
    path('checkout/', views.checkout, name='Checkout'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

]
