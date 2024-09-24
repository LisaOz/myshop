from django.urls import path
from . import views
app_name = "payment"

"""
URLs for the payments workflow
"""
urlpatterns = [
    path('process/', views.payment_process, name='process'), # vie that displays the order summary to the user, creates the Stripe checkout session, and redirects the user to the Stripe-hosted payment form
    path('completed/', views.payment_completed, name='completed'), # the view for Stripe to redirect the user if the payment is successful
    path('canceled/', views.payment_canceled, name='canceled'),
]