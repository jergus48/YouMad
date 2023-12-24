from django.db import models, IntegrityError
from django.contrib.auth.models import User
import json
import math
from django.db.models import Q
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os
from django.conf import settings
from io import BytesIO, StringIO
from django.core.mail import send_mail
from django.template.loader import render_to_string


from xhtml2pdf import pisa

import os
from django.template.loader import get_template
import pdfkit


from django.conf import settings

class Slider(models.Model):
    Title=models.CharField(max_length=50,null=True) 
    button_url=models.CharField(max_length=50,null=True, blank=True) 
    button_text=models.CharField(max_length=50,null=True) 
    main_image=models.ImageField(upload_to="slider/",null=True)
    announcement_bar=models.CharField(max_length=50,null=True) 
class Slide(models.Model):
    slider =models.ForeignKey(Slider, on_delete=models.CASCADE, default=1) 
    images = models.ImageField(upload_to="slider/")

  
    
  
   
    

class Products(models.Model): 
    name = models.CharField(max_length=60) 
    price = models.FloatField(default=0.0)
    discount=  models.IntegerField(default=0) 
  
    description = models.CharField( 
        max_length=250, default='', blank=True, null=True) 
    
  
    @staticmethod
    def get_product_by_id(id): 
        return Products.objects.get(id__in=id) 
  
    @staticmethod
    def get_all_products(): 
        return Products.objects.all() 
  
    
    def __str__(self):
        return self.name
class Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=1) 
    images = models.ImageField(upload_to="products/")



class Size(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product.name)+' - '+str(self.size)




class Shipping(models.Model):
    country=models.CharField(max_length=50, default='')
    def __str__(self):
        return self.country
class ShippingMethod(models.Model):
    country=models.ForeignKey(Shipping, 
                                on_delete=models.CASCADE, null=True) 
    name=models.CharField(max_length=50, default='')
    price=models.FloatField(default=0.0) 
    delivery_time =  models.CharField(max_length=100, default='',null=True)
    def __str__(self):
        return str(self.country.country)+' - '+str(self.name)


class Order(models.Model): 
    status_ordered=models.BooleanField(default=False) 
    status_sent = models.BooleanField(default=False) 
    order_price = models.FloatField(default=0.0)
    customer_first_name = models.CharField(max_length=50, default='')
    customer_last_name = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    mail = models.CharField(max_length=50, default='',null=True)
    street = models.CharField(max_length=150, default='')
    city = models.CharField(max_length=50, default='')
    zip_address = models.CharField(max_length=50, default='')
    shipping_method = models.ForeignKey(ShippingMethod, 
                                on_delete=models.CASCADE, null=True) 
    date = models.DateTimeField(default=timezone.now)
    invoice=models.FileField(upload_to='pdf_invoices/',null=True)
    
    
  
    def placeOrder(self): 
        self.save() 
    def get_order_total(self):
        total = 0
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.get_item_total()
        total += self.shipping_method.price
        if AdminInformations.objects.all()[0].DPH == True:
            total += (AdminInformations.objects.all()[0].dph_size*self.shipping_method.price)/(100-AdminInformations.objects.all()[0].dph_size )
        
            
        return total
    def __str__(self):
            return "Order #"+str(self.id)
    
class OrderItem(models.Model) :
    order = models.ForeignKey(Order, 
                                on_delete=models.CASCADE, null=True) 
    
    product_and_size = models.ForeignKey(Size, 
                                on_delete=models.CASCADE,null=True) 
    quantity = models.IntegerField(default=1)
   
    def get_item_total(self):
        discount = self.product_and_size.product.discount
        price=self.product_and_size.product.price

        total = self.quantity * price * (1 - discount / 100)
        
        if AdminInformations.objects.all()[0].DPH == True:
            total+=(AdminInformations.objects.all()[0].dph_size*total)/(100-AdminInformations.objects.all()[0].dph_size )
            
       
        return total

    def __str__(self):
        return self.product_and_size.product.name
    
class AdminInformations(models.Model):
    name=models.CharField(max_length=150, default='')
    
    phone = models.CharField(max_length=50, default='')
    mail = models.CharField(max_length=50, default='',null=True)
    country = models.CharField(max_length=50, default='')
    street = models.CharField(max_length=150, default='')
    city = models.CharField(max_length=50, default='')
    zip_address = models.CharField(max_length=50, default='')
    website=models.CharField(max_length=50, default='')
    ič_dph= models.CharField(max_length=50, null=True)
    dič= models.CharField(max_length=50, null=True,blank=True)
    ičo= models.CharField(max_length=50, null=True,blank=True)
    IBAN= models.CharField(max_length=50, default='',blank=True)
    stamp=models.ImageField(upload_to="",null=True,blank=True)
    DPH = models.BooleanField(default=False) 
    dph_size=models.FloatField(default=20.0)
    logo=models.ImageField(upload_to="")
    def __str__(self):
        return self.name
    class Meta:  
        verbose_name_plural = 'Admin Information'


@receiver(post_save, sender=OrderItem)
def update_order_price(sender, instance, **kwargs):
    order = instance.order
    order.order_price = round(order.get_order_total(), 2)
    orderId = order.id
    invoice_number = 2000000 + int(orderId)

    orderItems = OrderItem.objects.filter(order=orderId)
    shipping_method = order.shipping_method

    try:
        SupplierInformations = AdminInformations.objects.all()[0]
    except:
        SupplierInformations = ""
    
    for item in orderItems:
        item.discounted_price = item.product_and_size.product.price * (1 - item.product_and_size.product.discount / 100)*item.quantity
        if SupplierInformations!="" and SupplierInformations.DPH == True:
            
            item.dph=(SupplierInformations.dph_size*item.discounted_price)/(100-SupplierInformations.dph_size )
            
            item.price_with_dph=item.discounted_price+  item.dph
    if SupplierInformations!="" and SupplierInformations.DPH == True:
        shipping_method.dph=(SupplierInformations.dph_size*shipping_method.price)/(100-SupplierInformations.dph_size )
        shipping_method.price_with_dph=shipping_method.price + shipping_method.dph
        
        

        

 
    # ... (rest of your code to calculate order details)

    filename = '{}.pdf'.format("invoice-" + str(invoice_number))

    # Load the HTML template
    
    html_template = get_template('main/invoice-form.html')
    rendered_html = html_template.render({
        "order": order,
        "total_price":order.order_price,
        "orderItems": orderItems,
        "invoice_number": invoice_number,
        "shipping_method": shipping_method,
        "SupplierInformations": SupplierInformations,
    })

    # File path to save the PDF
    filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = os.path.join(filepath, filename)

    # Generate the PDF from HTML using xhtml2pdf
    with open(pdf_save_path, 'w+b') as f:
        pisaStatus = pisa.CreatePDF(rendered_html, dest=f)
    
    

    # Set the generated PDF file path in the Order object
    order.invoice = pdf_save_path
    
    order.save()


@receiver(post_save, sender=Order)
def send_email_on_order_status_change(sender, instance, created, **kwargs):
    if instance.status_sent :
        # The status_sent field was changed to True

        # Customize the email subject and content as needed
        subject = 'Your Mad order was sent'
        

        # Customize the HTML content for the email using a template
        html_message = render_to_string('main/orderSentMail.html', {'order': instance})
        
        # Set the sender and recipient email addresses
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.mail  # Assuming 'mail' is the email field in your Order model

        # Send the email
        send_mail(subject, "", from_email, [to_email], html_message=html_message)
      
    


