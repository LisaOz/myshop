from .cart import Cart


"""
In this context processor, the cart is initialised with the request object
and it made available for the templates as a 'cart' variable.
"""
def cart(request):
    return {'cart': Cart(request)}