from decimal import Decimal
from django.conf import settings
from shop.models import Product

"""
This is a Cart class to manage the shopping cart
"""
class Cart:
    def __init__(self, request):
        # Initialise the cart with the request object
        self.session = request.session # store the current session to be accessible to other methods of the Cart class
        cart = self.session.get(settings.CART_SESSION_ID) # take the cart from the current session it available
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} # create and save a cart as an empty dictonary in the session 
        self.cart = cart


    """
    This is the method to add or update product objects to the cart session. The default quantity is set to 1, and can ve overriden with the given quantity
    """
    def add(self, product, quantity=1, override_quantity=False):
        # add  the product to the cart snd uodate the quantity
        product_id = str(product.id)  #  JSON is used to serialise session data,  str key names only
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True # Mark the session to make sure is is saved


    """
    Method to remove producs from the cart dictionary and save() method updates the cart in the sassion.
    """
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # Method to iterate through the items in the cart to access the related product object from the database
    def __iter__(self):
        product_ids = self.cart.keys() # retrieve the Product instances present in the cart
        products = Product.objects.filter(id__in=product_ids) # include
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():# iterate over the cart values, 
            item['price'] = Decimal(item['price']) # convert the price back from str to decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

    """
    Method to return the total number of items in the cart
    """
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values()) # return the sum of quantities of all cart items
    

    """
    Method to calculate the total cost of all items in the cart
    """
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    """
    Method to clear the cart session
    """
    def clear(self):
        del self.session[settings.CART_SESSION_ID] # remove cart from session
        self.save()