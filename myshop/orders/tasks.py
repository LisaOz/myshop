"""
This file defines asynchronous tasks for the application. 
Celery will automatically discover and register tasks from this file when running the worker. 
Each task can be executed asynchronously in the background.
"""

from celery import shared_task
from django.core.mail import send_mail
from .models import Order


"""
Task 'order_created' for sending e-mail notification when an order is created
"""
@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order No {order.id}'
    message = (
        f'Dear {order.first_name}. \n\n'
        f'Your order has been registered.'
        f'Your order ID is {order.id}.'
    )
    mail_sent = send_mail(
        subject, message, 'admin@myshop.com', [order.email]
    )
    return mail_sent