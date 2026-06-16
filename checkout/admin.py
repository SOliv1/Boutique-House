from django.contrib import admin, messages
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Order, OrderLineItem


WAREHOUSE_CONTACT_NUMBER = '020 7946 0182'
ORDER_WAREHOUSE_COLUMNS = {
    'warehouse_status',
    'warehouse_sent_at',
    'warehouse_sent_by_id',
    'warehouse_sent_by_role',
}
ORDER_BASE_FIELDS = (
    'id',
    'order_number',
    'date',
    'full_name',
    'email',
    'delivery_cost',
    'order_total',
    'grand_total',
    'confirmation_email_sent_at',
)


def _table_columns(table_name):
    try:
        with connection.cursor() as cursor:
            return {
                column.name
                for column in connection.introspection.get_table_description(
                    cursor,
                    table_name,
                )
            }
    except Exception:
        return set()


def _warehouse_columns_available():
    return ORDER_WAREHOUSE_COLUMNS.issubset(
        _table_columns(Order._meta.db_table)
    )


def _lineitem_colour_column_available():
    return 'product_colour' in _table_columns(OrderLineItem._meta.db_table)


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

    def get_fields(self, request, obj=None):
        fields = ['product', 'product_size', 'quantity', 'lineitem_total']
        if _lineitem_colour_column_available():
            fields.insert(1, 'product_colour')
        return fields


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    actions = ('send_to_warehouse',)
    change_form_template = 'admin/checkout/order/change_form.html'

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid', 'confirmation_email_sent_at',
                       'warehouse_admin_reminder',
                       'warehouse_status',
                       'warehouse_sent_at', 'warehouse_sent_by',
                       'warehouse_sent_by_role')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid', 'confirmation_email_sent_at',
              'warehouse_admin_reminder',
              'warehouse_status', 'warehouse_sent_at',
              'warehouse_sent_by', 'warehouse_sent_by_role')

    list_display = ('order_number', 'date', 'full_name', 'email',
                    'confirmation_email_status',
                    'warehouse_dispatch_status',
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not _warehouse_columns_available():
            return queryset.only(*ORDER_BASE_FIELDS)
        return queryset

    def get_list_display(self, request):
        base = ['order_number', 'date', 'full_name', 'email',
                'confirmation_email_status']
        if _warehouse_columns_available():
            base.extend([
                'warehouse_dispatch_status',
                'warehouse_sent_by',
                'warehouse_sent_at',
            ])
        base.extend(['order_total', 'delivery_cost', 'grand_total'])
        return base

    def get_list_filter(self, request):
        filters = ['date', 'confirmation_email_sent_at']
        if _warehouse_columns_available():
            filters.extend([
                'warehouse_status',
                'warehouse_sent_at',
                'warehouse_sent_by',
            ])
        return filters

    def get_search_fields(self, request):
        fields = ['order_number', 'full_name', 'email', 'stripe_pid']
        if _lineitem_colour_column_available():
            fields.append('lineitems__product_colour')
        if _warehouse_columns_available():
            fields.extend([
                'warehouse_sent_by__username',
                'warehouse_sent_by__first_name',
                'warehouse_sent_by__last_name',
                'warehouse_sent_by_role',
            ])
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = [
            'order_number',
            'date',
            'delivery_cost',
            'order_total',
            'grand_total',
            'original_bag',
            'stripe_pid',
            'confirmation_email_sent_at',
        ]
        if _warehouse_columns_available():
            fields.extend([
                'warehouse_admin_reminder',
                'warehouse_status',
                'warehouse_sent_at',
                'warehouse_sent_by',
                'warehouse_sent_by_role',
            ])
        return fields

    def get_fields(self, request, obj=None):
        fields = [
            'order_number',
            'user_profile',
            'date',
            'full_name',
            'email',
            'phone_number',
            'country',
            'postcode',
            'town_or_city',
            'street_address1',
            'street_address2',
            'county',
            'delivery_cost',
            'order_total',
            'grand_total',
            'original_bag',
            'stripe_pid',
            'confirmation_email_sent_at',
        ]
        if _warehouse_columns_available():
            fields.extend([
                'warehouse_admin_reminder',
                'warehouse_status',
                'warehouse_sent_at',
                'warehouse_sent_by',
                'warehouse_sent_by_role',
            ])
        return fields

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not _warehouse_columns_available():
            actions.pop('send_to_warehouse', None)
        return actions

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['warehouse_admin_available'] = (
            _warehouse_columns_available()
        )
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    @admin.display(description='Confirmation email')
    def confirmation_email_status(self, obj):
        if obj.confirmation_email_sent_at:
            return f'Sent {obj.confirmation_email_sent_at:%d %b %Y %H:%M}'
        return 'Not sent'

    @admin.display(description='Warehouse / Delivery')
    def warehouse_dispatch_status(self, obj):
        if not _warehouse_columns_available():
            return 'Pending migration'
        if obj.warehouse_status == Order.WAREHOUSE_SENT:
            return format_html(
                '<strong style="color: #166534;">{}</strong>',
                'Sent',
            )
        return format_html(
            '<strong style="color: #991b1b;">{}</strong>',
            'Needs sending',
        )

    @admin.display(description='Warehouse reminder')
    def warehouse_admin_reminder(self, obj):
        if not obj:
            return '-'
        if not _warehouse_columns_available():
            return format_html(
                '<div style="padding: 14px 16px; border-left: 6px solid #991b1b; '
                'background: #fef2f2; color: #7f1d1d;">'
                '<strong>{}</strong>'
                '</div>',
                'Warehouse controls are pending database migration.',
            )
        if obj.warehouse_status == Order.WAREHOUSE_SENT:
            sent_at = (
                obj.warehouse_sent_at.strftime('%d %b %Y %H:%M')
                if obj.warehouse_sent_at
                else 'time not recorded'
            )
            sent_by = obj.warehouse_sent_by or 'Unknown user'
            return format_html(
                '<div style="padding: 14px 16px; border-left: 6px solid #166534; '
                'background: #f0fdf4; color: #14532d;">'
                '<strong>Sent to Warehouse / Delivery.</strong><br>'
                'Sent by {} on {}.<br>'
                '<span>{}</span><br>'
                '<span>Warehouse contact: {}</span>'
                '</div>',
                sent_by,
                sent_at,
                obj.warehouse_sent_by_role or 'Role not recorded',
                WAREHOUSE_CONTACT_NUMBER,
            )
        return format_html(
            '<div style="padding: 14px 16px; border-left: 6px solid #b45309; '
            'background: #fffbeb; color: #78350f;">'
            '<strong>Action needed:</strong> {}<br>'
            '<strong>Warehouse contact:</strong> {}'
            '</div>',
            'this order has not yet been sent to Warehouse / Delivery. Use '
            'the prominent button at the top of this order when it is ready '
            'for fulfilment.',
            WAREHOUSE_CONTACT_NUMBER,
        )

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

    def _mark_orders_sent_to_warehouse(self, request, queryset):
        if not _warehouse_columns_available():
            return 0, queryset.count()

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

        return updated_count, skipped_count

    @admin.action(description='Send selected orders to Warehouse / Delivery')
    def send_to_warehouse(self, request, queryset):
        updated_count, skipped_count = self._mark_orders_sent_to_warehouse(
            request,
            queryset,
        )

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/send-to-warehouse/',
                self.admin_site.admin_view(self.send_single_order_to_warehouse),
                name='checkout_order_send_to_warehouse',
            ),
        ]
        return custom_urls + urls

    def send_single_order_to_warehouse(self, request, object_id):
        order = self.get_object(request, object_id)
        change_url = reverse(
            'admin:checkout_order_change',
            args=[object_id],
        )

        if not order:
            self.message_user(
                request,
                'Order could not be found.',
                messages.ERROR,
            )
            return HttpResponseRedirect(change_url)

        updated_count, skipped_count = self._mark_orders_sent_to_warehouse(
            request,
            Order.objects.filter(pk=order.pk),
        )

        if updated_count:
            self.message_user(
                request,
                f'Order {order.order_number} sent to Warehouse / Delivery.',
                messages.SUCCESS,
            )
        elif skipped_count:
            self.message_user(
                request,
                f'Order {order.order_number} was already sent.',
                messages.WARNING,
            )

        return HttpResponseRedirect(change_url)


admin.site.register(Order, OrderAdmin)
