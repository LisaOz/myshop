import csv
import datetime
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.http import HttpResponse



# Register your models here.

"""

"""
def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html) # avoid auto-escape. Do not use on the inputs that come from the users!
    return ""
order_payment.short_description = "Stripe payment"


"""
Model to manage orders from the admin site.
ModelInline class is included as an inline in the OrderAdmin class, it allows to include a model on the same edit page as its related model.
"""
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


"""
Method to export the data into the CSV file
"""

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = (
        f'attachment; filename={opts.verbose_name}.csv'
    )
    response = HttpResponse(content_type='text/csv') # tell the browser to treat the response as a CSV file
    response['Content-Disposition'] = content_disposition #header to indicate that HTTP response contains an attached file
    writer = csv.writer(response) # create a CSV writer to write to the response object
    fields = [
        field
        for field in opts.get_fields() # deg the model fields dynamically
        if not field.many_to_many and not field.one_to_many
    ]
    # First row with the header info
    writer.writerow([field.verbose_name for field in fields]) # write the header row including the field names

    # write data rows, iterating over the QuerySer and writing a row for each returned object
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y') # output value for the csv has to be a string
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV' # display name for the action in the action's drop=down element of the admin site

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        order_payment,
        "created",
        "updated"
    ]

    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
