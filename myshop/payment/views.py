from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# Create your views here.

"""
Stripe instance created. Stripe module is imported and the Stripe API key and API version are set
"""
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION 

"""
Payment_process view.
"""
def payment_process(request):
    order_id = request.session.get('order_id') # The current Order object ID is retrieved with order_id session key, stored previously with order_create view
    order = get_object_or_404(Order, id=order_id) # the Order object for the given ID is retrieved. Exception is raised if no order found

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )

        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        # Stripe checkout session data
        session_data = {
            'mode': 'payment', # the mode of the checkout session
            'client_reference_id': order.id, # unique reference for this payment, to match with the order
            'success_url': success_url, # URL for Stripe to redirect the user to if the payment is successful
            'cancel_url': cancel_url,
            'line_items': [] # list that will be populated with the order items
        }

        # Add order items to the Stripe cjechout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'GBP', # Great Britain Pound
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )

        # if the method is POST, a Stripe checkout session is created
        session = stripe.checkout.Session.create(**session_data)

        # Redirect too Stripe payment form
        return redirect(session.url, code=303) # 303 status code is recommended to redirect web applications to a new URI after HTTP POST 
    
    else:
        return render(request, 'payment/process.html', locals())
    

"""
View for the payment success
"""
def payment_completed(request):
    return render(request, 'payment/completed.html')

"""
View for the canceled payment
"""
def payment_canceled(request):
    return render(request, 'payment/canceled.html')