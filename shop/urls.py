from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='AboutUs'),
    # path('contact-us/', views.contact_us, name='ContactUs'),
    path('products/<int:id>/', views.product_view, name='Products'),
    path('search/', views.search, name='Search'),
    path('tracker/', views.tracker, name='Tracker'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path("cart/", views.view_cart, name="view_cart"),
    path("update-cart/<int:cart_item_id>/", views.update_cart, name="UpdateCart"),
    path("remove-from-cart/<int:cart_item_id>/", views.remove_from_cart, name="RemoveFromCart"),
    # path("checkout/", views.checkout, name="Checkout"),
    # path("payment-success/", views.payment_success, name="PaymentSuccess"),

    # path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
    # path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment-success/', views.payment_success, name='payment_success'),

]
