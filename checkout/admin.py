from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid', 'confirmation_email_sent_at')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid', 'confirmation_email_sent_at')

    list_display = ('order_number', 'date', 'full_name', 'email',
                    'confirmation_email_status',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    search_fields = ('order_number', 'full_name', 'email', 'stripe_pid')
    search_help_text = (
        'Search by order number, customer name, email, or Stripe payment ID.'
    )
    list_filter = ('date', 'confirmation_email_sent_at')
    ordering = ('-date',)

    @admin.display(description='Confirmation email')
    def confirmation_email_status(self, obj):
        if obj.confirmation_email_sent_at:
            return f'Sent {obj.confirmation_email_sent_at:%d %b %Y %H:%M}'
        return 'Not sent'


admin.site.register(Order, OrderAdmin)
