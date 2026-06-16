from django.contrib import admin, messages
from django.utils import timezone

from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fields = (
        'product',
        'product_colour',
        'product_size',
        'quantity',
        'lineitem_total',
    )


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    actions = ('send_to_warehouse',)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid', 'confirmation_email_sent_at',
                       'warehouse_sent_at', 'warehouse_sent_by',
                       'warehouse_sent_by_role')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid', 'confirmation_email_sent_at',
              'warehouse_status', 'warehouse_sent_at',
              'warehouse_sent_by', 'warehouse_sent_by_role')

    list_display = ('order_number', 'date', 'full_name', 'email',
                    'confirmation_email_status',
                    'warehouse_status',
                    'warehouse_sent_by',
                    'warehouse_sent_at',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    search_fields = (
        'order_number',
        'full_name',
        'email',
        'stripe_pid',
        'lineitems__product_colour',
        'warehouse_sent_by__username',
        'warehouse_sent_by__first_name',
        'warehouse_sent_by__last_name',
        'warehouse_sent_by_role',
    )
    search_help_text = (
        'Search by order number, customer, email, Stripe payment ID, colourway, '
        'or warehouse sender.'
    )
    list_filter = (
        'date',
        'confirmation_email_sent_at',
        'warehouse_status',
        'warehouse_sent_at',
        'warehouse_sent_by',
    )
    ordering = ('-date',)

    @admin.display(description='Confirmation email')
    def confirmation_email_status(self, obj):
        if obj.confirmation_email_sent_at:
            return f'Sent {obj.confirmation_email_sent_at:%d %b %Y %H:%M}'
        return 'Not sent'

    def _warehouse_user_role(self, user):
        role_parts = []
        if user.is_superuser:
            role_parts.append('Superuser')
        elif user.is_staff:
            role_parts.append('Staff')
        else:
            role_parts.append('User')

        group_names = list(user.groups.values_list('name', flat=True))
        if group_names:
            role_parts.append(f'Groups: {", ".join(group_names)}')

        return ' | '.join(role_parts)

    @admin.action(description='Send selected orders to Warehouse / Delivery')
    def send_to_warehouse(self, request, queryset):
        sent_at = timezone.now()
        role = self._warehouse_user_role(request.user)
        updated_count = 0
        skipped_count = 0

        for order in queryset:
            if order.warehouse_status == Order.WAREHOUSE_SENT:
                skipped_count += 1
                continue

            order.warehouse_status = Order.WAREHOUSE_SENT
            order.warehouse_sent_at = sent_at
            order.warehouse_sent_by = request.user
            order.warehouse_sent_by_role = role
            order.save(update_fields=[
                'warehouse_status',
                'warehouse_sent_at',
                'warehouse_sent_by',
                'warehouse_sent_by_role',
            ])
            updated_count += 1

        if updated_count:
            self.message_user(
                request,
                f'{updated_count} order(s) sent to Warehouse / Delivery.',
                messages.SUCCESS,
            )
        if skipped_count:
            self.message_user(
                request,
                f'{skipped_count} order(s) were already sent.',
                messages.WARNING,
            )


admin.site.register(Order, OrderAdmin)
