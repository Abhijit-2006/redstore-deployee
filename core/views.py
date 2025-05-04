from django.shortcuts import render,redirect,get_object_or_404
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm,CustomerForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import E_com,Cart,CustomerDetail,Order
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# from .models import Cart




#===============For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
#=========================================================

#================ Forgot Password ======================
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse



# Create your views here.
def index(request):
    return render(request,'core/index.html')

def product(request):
    return render(request, 'core/products.html')



def ProductDetails(request, id):
    dc = get_object_or_404(E_com, pk=id)  # Ensures proper error handling
    return render(request, 'core/ProductDetails.html', {'dc': dc})




def Men(request):
    dc = E_com.objects.filter(category='MEN')
    return render(request,'core/Men.html', {'dc':dc})

def Womens(request):
    dc = E_com.objects.filter(category='WOMEN')
    return render(request,'core/Womens.html', {'dc':dc})



# =====================================================================================================


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                messages.success(request,'Registration Successfull !!')
                email = request.POST['email']
                user = User.objects.filter(email=email).first()
                if user:
                    send_mail(
                        'Registration Successfull',
                        f'Thank you for choosing us!!',
                        'fordjangopproject@gmail.com',  # Use a verified email address
                        [email],
                        fail_silently=False,
                    )

                return redirect('registration')    
        else:
            mf  = RegistrationForm()
        return render(request,'core/registration.html',{'mf':mf})
    else:
        return redirect('profile')

def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login ,if so it will show login option
        if request.method == 'POST':       # otherwise it will redirect to the profile page 
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'core/login.html',{'mf':mf})
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
                messages.success(request,'Profile Updated Successfully !!')
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'core/profile.html',{'name':request.user,'mf':mf})
    else:                                                # request.user returns the username
        return redirect('login')

def log_out(request):
    logout(request)
    return redirect('login')


def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'core/changepassword.html',{'mf':mf})
    else:
        return redirect('login')                                      # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'core/changepassword.html',{'mf':mf})
    else:
        return redirect('login')






# ============================ Add To Cart ====================================

def add_to_cart(request,id):
    if request.user.is_authenticated:
        product = E_com.objects.get(pk=id)
        user = request.user
        Cart(user=user,product=product).save()
        messages.success(request, "Product added to cart successfully!")

        return redirect('ProductDetails', id)
    else:
        return redirect('login')

@login_required(login_url='/login/')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    return render(request, 'core/view_cart.html', {'cart_items': cart_items,'total':total,'final_price':final_price})


def add_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart,pk=id)
        product.quantity+=1
        product.save()
        return redirect('viewcart')
    else:
        return redirect('login')

def delete_quantity(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart,pk=id)
        if product.quantity>1:
            product.quantity-=1
            product.save()
        return redirect('viewcart')
    else:
        return redirect('login')
    

def delete_cart(request,id):
        de = Cart.objects.get(pk=id)
        de.delete()
        return redirect('viewcart')
    
    


# ================================ Address Page =========================
def address(request):
    if request.method == 'POST':
            aj =CustomerForm(request.POST)
            if aj.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= aj.cleaned_data['name']
                address= aj.cleaned_data['address']
                city= aj.cleaned_data['city']
                state= aj.cleaned_data['state']
                pincode= aj.cleaned_data['pincode']  
                CustomerDetail(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        aj =CustomerForm()
        address = CustomerDetail.objects.filter(user=request.user)
    return render(request,'core/address.html',{'mf':aj,'address':address})


def delete_address(request,id):
        de = CustomerDetail.objects.get(pk=id)
        de.delete()
        return redirect('address')



# ============================== Checkout Page ==============================

def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = CustomerDetail.objects.filter(user=request.user)
  
    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

def payment(request):

    if request.method=='POST':
        selected_address_id = request.POST.get('selected_address')
        print('=========',selected_address_id)
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = CustomerDetail.objects.filter(user=request.user)


  #================= Paypal Code =====================
   
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
        'amount': final_price,    #: The amount of money to be charged for the transaction. 
        'item_name': 'E_com',       # Describes the item being purchased.
        'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
        'return_url': f"http://{host}{reverse('paymentsuccess',args=[selected_address_id])}",     #The URL where the customer will be redirected after a successful payment. 
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    

  #================= Paypal Code  End =====================

    return render(request,'core/payment.html',{'paypal':paypal_payment})


# ==================== Payment Success Page =====================================
def payment_success(request,selected_address_id):

    user= request.user
    address_data = CustomerDetail.objects.get(pk=selected_address_id)
    cart=Cart.objects.filter(user=request.user)
    for cart in cart:
        Order(user=user,customer=address_data,quantity=cart.quantity,E_com=cart.product).save()
        cart.delete()
    return render(request,'core/payment_success.html')


# ==================== Payment Failed Page =====================================

def payment_failed(request):
    return render(request,'core/payment_failed.html')


# ========================= Order Page ==================================

def order(request):
    ord= Order.objects.filter(user=request.user)
    return render(request,'core/order.html',{'ord':ord})



#========================================== Buy Now ========================================================
@login_required(login_url='login')
def buynow(request,id):
    de = E_com.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + de.discounted_price
    
    address = CustomerDetail.objects.filter(user=request.user)

    return render(request, 'core/buynow.html', {'final_price':final_price,'address':address,'de':de})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    product = E_com.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + product.discounted_price
    
    address = CustomerDetail.objects.filter(user=request.user)
    
    
  #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Pet',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================
    

    return render(request, 'core/payment.html', {'final_price':final_price,'address':address,'product':product,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = CustomerDetail.objects.get(pk=selected_address_id,)
    
    product = E_com.objects.get(pk=id)
    Order(user=user,customer=customer_data,E_com=product,quantity=1).save()
   
    return render(request,'core/buynow_payment_success.html')



#================================== Forget Password ====================================================

def forgot_password(request):          
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'fordjangopproject@gmail.com',  # Use a verified email address
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'please enter valid email address')
    return render(request, 'core/forgot_password.html')
                                         
    # return render(request,'core/forgot_password.html',)

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')