from django.urls import path
from . import views


#------ To incude Media file ---------------
from django.conf import settings
from django.conf.urls.static import static
#-----------------------------------------------

urlpatterns = [
    path('',views.index,name="index"),
    
    path('products/', views.product, name="products"),
    
    path('men/', views.Men, name="Men"),
    
    path('womens/', views.Womens, name="Womens"),
    
    path('productdetails/<int:id>/',views.ProductDetails, name="ProductDetails"),
    
    path('registration/',views.registration,name='registration'),
    
    path('login/',views.log_in,name='login'),
    
    path('profile/',views.profile,name='profile'),
    
    path('logout/',views.log_out, name="logout"),
    
    path('changepassword/',views.changepassword, name="changepassword"),
    
    path('view_cart/',views.view_cart, name="viewcart"),
    
    path('add_to_cart/<int:id>',views.add_to_cart, name="addtocart"),
    
    path('add_quantity/<int:id>',views.add_quantity, name="add_quantity"),
    
    path('delete_quantity/<int:id>',views.delete_quantity, name="delete_quantity"),
    
    path('delete_cart/<int:id>',views.delete_cart, name="deletecart"),
    
    path('address/',views.address,name='address'),
    
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),
    
    path('checkout/',views.checkout,name='checkout'),
    
    path('payment_success/<int:selected_address_id>',views.payment_success,name='paymentsuccess'),
    
    path('payment_failed/',views.payment_failed,name='paymentfailed'),
    
    path('payment/',views.payment,name='payment'),
    
    path('order/',views.order,name='order'),
    
    path('buynow/<int:id>',views.buynow,name='buynow'),
    
    path('buynow_payment/<int:id>',views.buynow_payment,name='buynowpayment'),
    
    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),
    
    path('forgotpassword/',views.forgot_password, name="forgotpassword"),
    
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
    
    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),

]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)