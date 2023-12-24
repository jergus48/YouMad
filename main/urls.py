from django.urls import path
from .views import *
from django.conf.urls.static import static
app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products-<int:id>/',ProductView.as_view(),name='productView'),
    path('search/', searchResults.as_view(),name="searchResults"),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('about/', About.as_view(),name="about"),
    path('cart/',ViewCart.as_view(),name='cart'),
    path('succesful-order/<int:id>/', SuccesfulOrder.as_view(),name="SuccesfulOrder"),
    
    path('addtocart/',AddToCart,name='AddToCart'),
    path('get-size-quantity/',get_size_quantity,name='SizeQuantity'),
    path('update-cart/',update_cart,name='update_cart'),
    path('create-order/',CreateOrder,name='order'),
    path('get_shipping_rates/', get_shipping_rates, name='get_shipping_rates'),
    path('charge/', Charge,name="charge"),
    
    path('invoice/', invoice,name="invoice"),
    
   
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)