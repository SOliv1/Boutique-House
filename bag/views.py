from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from products.models import Product


def _variant_key(size, colour):
    return f'{size or "no-size"}::{colour or "no-colour"}'


def _variant_label(size, colour):
    details = []
    if colour:
        details.append(colour)
    if size:
        details.append(f'size {size.upper()}')
    return ', '.join(details)


def _ensure_variant_bag_item(bag, item_id):
    if item_id not in bag:
        bag[item_id] = {'items_by_variant': {}}
    elif isinstance(bag[item_id], int):
        bag[item_id] = {
            'items_by_variant': {
                _variant_key(None, None): {
                    'quantity': bag[item_id],
                    'size': None,
                    'colour': None,
                },
            },
        }
    elif 'items_by_variant' not in bag[item_id]:
        variants = {}
        for size, quantity in bag[item_id].get('items_by_size', {}).items():
            variants[_variant_key(size, None)] = {
                'quantity': quantity,
                'size': size,
                'colour': None,
            }
        bag[item_id] = {'items_by_variant': variants}


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    colour = request.POST.get('product_colour') or None
    bag = request.session.get('bag', {})

    if size or colour:
        key = _variant_key(size, colour)
        label = _variant_label(size, colour)
        _ensure_variant_bag_item(bag, item_id)
        if key in bag[item_id]['items_by_variant'].keys():
            bag[item_id]['items_by_variant'][key]['quantity'] += quantity
            messages.success(request,
                             (f'Updated {label} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_variant"][key]["quantity"]}'))
        else:
            bag[item_id]['items_by_variant'][key] = {
                'quantity': quantity,
                'size': size,
                'colour': colour,
            }
            messages.success(request,
                             (f'Added {label} '
                              f'{product.name} to your bag'))
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    colour = request.POST.get('product_colour') or None
    variant_key = request.POST.get('variant_key') or _variant_key(size, colour)
    bag = request.session.get('bag', {})

    item_data = bag.get(item_id)

    if isinstance(item_data, dict) and 'items_by_variant' in item_data:
        label = _variant_label(size, colour)
        if quantity > 0:
            bag[item_id]['items_by_variant'][variant_key]['quantity'] = quantity
            messages.success(request,
                             (f'Updated {label} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_variant"][variant_key]["quantity"]}'))
        else:
            del bag[item_id]['items_by_variant'][variant_key]
            if not bag[item_id]['items_by_variant']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed {label} '
                              f'{product.name} from your bag'))
    elif size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_size"][size]}'))
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag.pop(item_id)
            messages.success(request,
                             (f'Removed {product.name} '
                              f'from your bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


@require_POST
def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        colour = request.POST.get('product_colour') or None
        variant_key = request.POST.get('variant_key') or _variant_key(size, colour)
        bag = request.session.get('bag', {})

        item_data = bag.get(item_id)

        if isinstance(item_data, dict) and 'items_by_variant' in item_data:
            del bag[item_id]['items_by_variant'][variant_key]
            if not bag[item_id]['items_by_variant']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed {_variant_label(size, colour)} '
                              f'{product.name} from your bag'))
        elif size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('view_bag'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
