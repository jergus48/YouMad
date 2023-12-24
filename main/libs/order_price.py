from ..models import *
def calculate(order_items,shipping_method):
    order_price=0
    for item in order_items:
        discount = item.product_and_size.product.discount
        price=item.product_and_size.product.price

        total = item.quantity * price * (1 - discount / 100)
        
        if AdminInformations.objects.all()[0].DPH == True:
            total+=(AdminInformations.objects.all()[0].dph_size*total)/(100-AdminInformations.objects.all()[0].dph_size )
        order_price+=total
    order_price += shipping_method.price
    if AdminInformations.objects.all()[0].DPH == True:
        order_price += (AdminInformations.objects.all()[0].dph_size*shipping_method.price)/(100-AdminInformations.objects.all()[0].dph_size )
    return order_price