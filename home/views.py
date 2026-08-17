from django.db import DatabaseError
from django.shortcuts import render
from django.db import OperationalError, ProgrammingError
from django.views.decorators.http import require_http_methods

from checkout.models import Order

from .models import HomePageHero, HomePromotion
from .seasonal_covers import get_seasonal_cover


def index(request):
    """ A view to return the index page """
    try:
        home_hero = HomePageHero.objects.filter(is_active=True).first()
        home_promotion = HomePromotion.objects.filter(is_active=True).first()
    except (OperationalError, ProgrammingError):
        home_hero = None
        home_promotion = None
    context = {
        'home_hero': home_hero,
        'home_promotion': home_promotion,
        'seasonal_cover': get_seasonal_cover(),
    }
    return render(request, 'home/index.html', context)


def privacy_policy(request):
    """Return the Boutique House privacy policy."""
    return render(request, 'legal/privacy_policy.html')


def terms_and_conditions(request):
    """Return the Boutique House terms and conditions."""
    return render(request, 'legal/terms.html')


def delivery_information(request):
    """Return delivery options and restrictions."""
    return render(request, 'deliveries/delivery.html')


@require_http_methods(['GET', 'POST'])
def track_order(request):
    """Look up an order using its number and matching customer email."""
    order = None
    lookup_attempted = request.method == 'POST'
    order_number = request.POST.get('order_number', '').strip().upper()
    email = request.POST.get('email', '').strip()
    lookup_error = None

    if lookup_attempted:
        if not order_number or not email:
            lookup_error = 'Enter both your order number and email address.'
        else:
            try:
                order = (
                    Order.objects.prefetch_related('lineitems__product')
                    .filter(
                        order_number__iexact=order_number,
                        email__iexact=email,
                    )
                    .first()
                )
            except DatabaseError:
                lookup_error = (
                    'Order tracking is temporarily unavailable. '
                    'Please try again shortly.'
                )
            if order is None and lookup_error is None:
                lookup_error = (
                    'We could not find an order matching those details. '
                    'Please check your confirmation email and try again.'
                )

    context = {
        'order': order,
        'lookup_attempted': lookup_attempted,
        'lookup_error': lookup_error,
        'submitted_order_number': order_number,
        'submitted_email': email,
    }
    return render(request, 'deliveries/track_order.html', context)
