from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, add_to_cart, remove_from_cart, cart_detail, buy_now, buy_all, checkout, delete_product_image
from . import views

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/delete-image/<int:image_id>/', delete_product_image, name='delete_product_image'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('buy/<int:product_id>/', buy_now, name='buy_now'),  # URL for buying a single item
    path('buy_all/', buy_all, name='buy_all'),  # URL for buying all items in the cart
    path('checkout/', checkout, name='checkout'),
    path('payment/', views.PaymentFormView.as_view(), name='payment_form'),  # Payment form view
    path('payment/process/', views.PaymentProcessView.as_view(), name='payment_process'),  # Payment process view
    path('thank-you/', views.ThankYouView.as_view(), name='thank_you'),  # Thank You page
]
