from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.core.mail import send_mail

from xhtml2pdf import pisa
from .models import *
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponseRedirect
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import os
import pdfkit 
from .libs import search_products,announcement,stripeFunctions,dph,order_price

from django.template.loader import render_to_string
from django.utils.html import strip_tags
#Views:
#Index
class IndexView(View):
    """
    Index view
    """
    template_name = 'main/index.html'
    
    def get(self, request):
        """
        Displays the index page.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        products = Products.objects.filter(size__quantity__gt=0).distinct()
        for product in products:
            try:
                product.image=Image.objects.filter(product=product)[0]
                discounted_price = product.price * (1 - product.discount / 100)
               
            
                
                discounted_price=dph.calculate(discounted_price)
                
                
                product.discounted_price=round(discounted_price, 2)

            except:
                pass
           
     
        slider=Slider.objects.all()[0]
        slides=Slide.objects.filter(slider=slider)
        slider.first_slide=slides[0]
        slides=slides[1:]
        ab=announcement.bar()
        return render(request, self.template_name,{'products':products,'slider':slider,"slides":slides,"announcement_bar":ab})

    
#About
class About(View):
    """
    Index view
    """
    template_name = 'main/about.html'
    
    def get(self, request):
        """
        Displays the index page.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        ab=announcement.bar()
        return render(request, self.template_name,{"announcement_bar":ab})

#Search Results
class searchResults(View):
    """
    View for handling adding to cart
    """
    template_name = 'main/searchResultsView.html'
    
    def get(self, request):
       
        """
        Displays the Search results View.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
     
        if "q" in request.GET:
            query=request.GET.get("q")
            results=search_products.results(query)
        else:
            query=""
            results=[]
        return render(request, self.template_name,{"results":results,"query":query})

   


#Product View

class ProductView(View):
    """
    View for handling adding to cart
    """
    template_name = 'main/ProductView.html'
    
    def get(self, request,id):
       
        """
        Displays the product View.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        
        
       
        product=Products.objects.get(id=id)
        discounted_price = product.price * (1 - product.discount / 100)
        sizes = Size.objects.filter(product=product).exclude(quantity=0)
  
        images=Image.objects.filter(product=product)
        image=images[0]
        images=images[1:]
      
        product.price=dph.calculate(product.price)
        discounted_price=dph.calculate(discounted_price)
        
        product.price=round(product.price, 2)
        discounted_price=round(discounted_price, 2)
        ab=announcement.bar()
        return render(request, self.template_name,{'product':product,'sizes':sizes,'images':images,'imageone':image,'discounted_price':discounted_price,"announcement_bar":ab})

 #Checkout

class Checkout(View):
    """
    View for handling user registration and new member creation.
    """
    template_name = 'main/checkout.html'
    
    def get(self, request):
        """
        Displays the index page.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        cart_control(request)
        cart = request.session.get('cart', {}) 
        price=0  
        
        for size_id, quantity in cart.items():
        
            size = Size.objects.get(id=size_id)
                
            price += size.product.price*(1 - size.product.discount / 100)*quantity

        
        price=dph.calculate(price)
        price=round(price, 2)
        return render(request, self.template_name,{'price': price})
#Cart
class ViewCart(View):
    """
    View for handling user registration and new member creation.
    """
    template_name = 'main/cart.html'
    
    def get(self, request):
        """
        Displays the index page.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        cart_control(request)
        cart = request.session.get('cart', {}) 
        items = []  
        total_price=0
        total_items=0
        for size_id, quantity in cart.items():
            try:
                size = Size.objects.get(id=size_id)
                product_name = size.product.name
            
                max_quantity = size.quantity
                price = size.product.price*(1 - size.product.discount / 100)*quantity
                price=dph.calculate(price)
                price = round(price, 2)
                total_price+=price
                total_items+=quantity
                image=Image.objects.filter(product=size.product )[0].images.url
                items.append({'product': product_name,'image_url':image, 'size': size, 'quantity': quantity,'price':price,'max_quantity':max_quantity})
            except Size.DoesNotExist:
                pass
        total_price=round(total_price, 2)
        
        return render(request, self.template_name,{'cart_items': items, "total_price":total_price,"total_items":total_items})

#Succesful Order

class SuccesfulOrder(View):
    """
    View for handling user registration and new member creation.
    """
    template_name = 'main/succesful-order.html'
    
    def get(self, request,id):
        """
        Displays the index page.

        Args:
            request: HTTP request object.

        Returns:
            Rendered template response.
        """
        order=Order.objects.get(id=id)
        shipping_method=order.shipping_method
        items=OrderItem.objects.filter(order=order)
        shipping_method.price=dph.calculate(shipping_method.price)
        total_price=0
        for item in items:
            productID= item.product_and_size.product
            image=Image.objects.filter(product=productID)[0]
            item.image = image.images.url
            size=item.product_and_size
            quantity=item.quantity
            price = size.product.price*(1 - size.product.discount / 100)*quantity
            price=price=dph.calculate(price)
            price = round(price, 2)
            total_price+=price
            item.price= price
        total_price+=shipping_method.price
        total_price=round(total_price, 2)
        return render(request, self.template_name,{'order_items': items,'order':order,"shipping_method":shipping_method,"total_price":total_price})

#Json Responses

def AddToCart(request):
    if request.GET:
        
        size_id = request.GET.get('size')
        quantity = int(request.GET.get('quantity'))

       
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if size_id in cart:
           
            cart[size_id] += quantity
        else:
            
            cart[size_id] = quantity

        request.session.modified = True 
        product=Size.objects.get(id=size_id).product.id
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
        
def get_size_quantity(request):
    
    size_id = request.GET.get("size")
    size = Size.objects.get(id=size_id)
    quantity = size.quantity
    if 'cart'  in request.session:
        cart = request.session.get('cart', {})

        if size_id in cart:
          
            quantity_in_cart = cart[size_id]
            quantity-=quantity_in_cart
        
    return JsonResponse({"quantity": quantity})



def update_cart(request):
    if request.method == 'GET':
        size_id = request.GET.get('size')
        new_quantity = int(request.GET.get('new_quantity'))
        
        cart = request.session.get('cart', {})
      
        if new_quantity == 0:
        
            if size_id in cart:
                del cart[size_id]
             
     
        else:
            cart[size_id] = new_quantity

      
        request.session['cart'] = cart
        request.session.modified = True
      
        return JsonResponse({"quantity": new_quantity})

    return JsonResponse({"quantity": new_quantity})





def get_shipping_rates(request):
    shipping_data = {}
    countries = Shipping.objects.all()
    for country in countries:
        methods = ShippingMethod.objects.filter(country=country)
        shipping_data[country.country] = {}
        for method in methods:
            
            shipping_data[country.country][method.name] = method.price
            
            shipping_data[country.country][method.name]=dph.calculate(method.price)
    return JsonResponse(shipping_data)





def Charge(request):
    data = json.loads(request.body.decode('utf-8'))
    amount =int(data.get('price') * 100)
    customer_identifier = data.get('customer_identifier')  # Unique identifier for the customer or session
    
    if 'order_number' not in request.session:
        order=Order.objects.create()
        order.save()
      
        request.session['order_number'] = order.id
        order_number=order.id
       
    else:
        order_number=request.session['order_number']
     
        

    stripe.api_key = settings.STRIPE_SECRET_KEY

    customer=stripeFunctions.get_create_customer(customer_identifier)
    existing_payment_intent = stripeFunctions.retrieve_existing_payment_intent(customer)




    if existing_payment_intent and existing_payment_intent.status not in ['succeeded']:
        # Update the existing payment intent with the new amount
       
        existing_payment_intent = stripe.PaymentIntent.modify(
            existing_payment_intent.id,
            amount=amount,
        )
        return JsonResponse({'client_secret': existing_payment_intent.client_secret,'order_number':order_number})

    # If no existing payment intent, create a new one
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='eur',
        customer=customer,  # Use the customer identifier to associate with the customer
        automatic_payment_methods={'enabled': True}
    )
    
    return JsonResponse({'client_secret': payment_intent.client_secret,'order_number':order_number})


def confirmation_mail(order,mail):
    orderId = order.id
   
    #confirmation mail
    orderItems = OrderItem.objects.filter(order=orderId)
    shipping_method = order.shipping_method
    shipping_method.price=dph.calculate(shipping_method.price)
    
    for item in orderItems:
        price = item.product_and_size.product.price * (1 - item.product_and_size.product.discount / 100)*item.quantity
 
        price=dph.calculate(price)
        price = round(price, 2)
        item.discounted_price = price
        item.name=item.product_and_size.product.name
        item.image= Image.objects.filter(product=item.product_and_size.product )[0]
    order_data ={
        "order": order,
        "total_price":order.order_price,
        "orderItems": orderItems,
        "shipping_method": shipping_method,
        "SupplierInformations": AdminInformations.objects.all()[0],
    }    
    html_message = render_to_string('main/order_confirmation_email.html', order_data)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        'Order Confirmation',
        plain_message,
        'info2mad@gmail.com',  
        [mail,'info2mad@gmail.com'], 
        html_message=html_message,
    )   
   

def CreateOrder(request):
 
    mail = request.POST.get('mail')
    country = request.POST.get('country')
    
    shipping_name=request.POST.get('shipping_method')
    country_id= Shipping.objects.get(country=country)
    shipping_method = ShippingMethod.objects.get(country=country_id,name=shipping_name)
    
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    city = request.POST.get('city')
    street = request.POST.get('street')
    postal_code = request.POST.get('postalcode')
    phone = request.POST.get('phone')
    order_number=request.POST.get('order_number')
    
    order=Order.objects.get(id=order_number)
    
    order.mail=mail
    order.status_ordered=True
    order.customer_first_name=first_name
    order.customer_last_name=last_name
    order.country=country
    order.phone=phone
    order.city=city
    order.street=street
    order.zip_address=postal_code
    order.shipping_method=shipping_method
    
    
    # delete items from cart
    cart = request.session.get('cart', {})
    order_items = []
    for size_id, Quantity in cart.items():
        
        size = Size.objects.get(id=size_id)
        order_items.append(OrderItem(order=order, product_and_size=size, quantity=Quantity))
        size.quantity-=Quantity
        size.save()

    OrderItem.objects.bulk_create(order_items)
    order.order_price=order_price.calculate(order_items,shipping_method)
    order.save()    
    if 'order_number' in request.session:
        del request.session['order_number']
    if 'cart' in request.session:
        del request.session['cart']
    request.session.modified = True

    confirmation_mail(order,mail)
    invoice(order)
    return JsonResponse({"succes":True})
def cart_control(request):
    
    cart = request.session.get('cart', {})
    cart_copy = cart.copy()
   

    for size_id, cart_quantity in cart_copy.items():
        try:
            product = Size.objects.get(id=size_id)
            
            if product.quantity == 0:
                del cart[size_id]
            elif product.quantity < cart_quantity:
                cart[size_id] = product.quantity
        except Size.DoesNotExist:
         
            del cart[size_id]

  
        

    # Update the session with the modified cart
    request.session['cart'] = cart


def invoice(order):
   
   
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

