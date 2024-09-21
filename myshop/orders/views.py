from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem

# Create your views here.

"""
Order_create view
"""
def order_create(request):
    cart = Cart(request) # get the current cart from the session cart
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart: # iterate over all items in the cart and create a new order in the database 
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
                # To clear the cart
                cart.clear()
                return render(
                    request, 
                    'orders/order/created.html', 
                    {'order': order}
                )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )