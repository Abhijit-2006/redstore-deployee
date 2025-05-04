from django.contrib import admin
from .models import CustomerDetail,E_com,Cart,Order


# Register your models here.

@admin.register(CustomerDetail)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']


@admin.register(E_com)
class E_comAdmin(admin.ModelAdmin):
    list_display= ['id','name','category','small_description','description','original_price','discounted_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity','size']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','E_com','quantity','order_at','status']