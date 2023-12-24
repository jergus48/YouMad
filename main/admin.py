from django.contrib import admin
from .models import Products,OrderItem,Order, Size, ShippingMethod, Shipping,AdminInformations,Slider,Slide
# Register your models here.
from django import forms




from django import forms
from .models import OrderItem

from django import forms
from .models import OrderItem, Products, Size,Image

class SlideInline(admin.TabularInline):  # You can use StackedInline if you prefer a different layout
    model = Slide
    extra = 1  


class ImageInline(admin.TabularInline):  # You can use StackedInline if you prefer a different layout
    model = Image
    extra = 1  

class SizeInline(admin.TabularInline):  # You can use StackedInline if you prefer a different layout
    model = Size
    extra = 1  # The number of empty Size instances to display

class SliderAdmin(admin.ModelAdmin):
    inlines = [SlideInline]
    list_display=('Title','button_url','button_text','main_image')
    def has_add_permission(self, request):
        # Check if any instance of the model exists
        return not Slider.objects.exists()
class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline,ImageInline]
    list_display=('name','price','discount')
class OrderItemInline(admin.TabularInline):  # You can use StackedInline if you prefer a different layout
    model = OrderItem
    extra = 1  # The number of empty OrderItem instances to display

    # Customize the form fields
    

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['order_price']
    search_fields = ['mail__icontains','mail']
    list_display = ('status_sent','id', 'order_price','customer_first_name','customer_last_name','phone','mail','country','street','city','zip_address','date')
    
    exclude = ('status_ordered',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(status_ordered=False)

class ShippingMethodInline(admin.TabularInline):
    model=ShippingMethod
    extra=1
class ShippingAdmin(admin.ModelAdmin):
    inlines=[ShippingMethodInline]


class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Check if any instance of the model exists
        return not AdminInformations.objects.exists()

# Register your model with the custom admin class
admin.site.register(AdminInformations, SingletonModelAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Slider,SliderAdmin)