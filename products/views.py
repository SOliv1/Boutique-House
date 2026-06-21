from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Collection
from .forms import ProductForm

# Create your views here.


def _absolute_media_url(request, uploaded_image=None, external_url=None):
    if external_url:
        return request.build_absolute_uri(external_url)
    if uploaded_image:
        return request.build_absolute_uri(uploaded_image.url)
    return None


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    collections = None
    current_collection = None
    moods_board_collection = None
    moods_board_products = None
    current_promotion = None
    sort = None
    direction = None

    try:
        if request.GET:
            if 'sort' in request.GET:
                sortkey = request.GET['sort']
                sort = sortkey
                if sortkey == 'name':
                    sortkey = 'lower_name'
                    products = products.annotate(lower_name=Lower('name'))
                if sortkey == 'category':
                    sortkey = 'category__name'
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

            if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)

            if 'collection' in request.GET:
                collection_names = request.GET['collection'].split(',')
                if 'moods_board' in collection_names:
                    return redirect('https://soliv1.github.io/moodsboard-reflections-family/#/')
                products = products.filter(collection__name__in=collection_names)
                collections = Collection.objects.filter(name__in=collection_names)

                collections_count = collections.count()
                products.first()

                if collections_count == 1:
                    current_collection = collections.first()
                    if current_collection.name == 'garden':
                        moods_board_collection = Collection.objects.filter(
                            name='moods_board'
                        ).first()
                        moods_board_products = Product.objects.filter(
                            collection__name='moods_board'
                        )
                        moods_board_products.first()

            if 'promotion' in request.GET:
                promotion = request.GET['promotion']
                promotion_filters = {
                    'new_arrivals': ('is_new_arrival', 'New Arrivals'),
                    'deals': ('is_special_offer', 'Special Deals'),
                    'clearance': ('is_clearance', 'Clearance'),
                }
                if promotion in promotion_filters:
                    field_name, current_promotion = promotion_filters[promotion]
                    products = products.filter(**{field_name: True})

            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(request, "You didn't enter any search criteria!")
                    return redirect(reverse('products'))

                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)

        # Force row-level evaluation so missing columns/schema drift are
        # handled here instead of failing later in template rendering.
        products.first()
    except DatabaseError:
        messages.error(
            request,
            'Products are temporarily unavailable. Please try again shortly.',
        )
        products = Product.objects.none()
        categories = None
        collections = None
        current_collection = None
        moods_board_collection = None
        moods_board_products = None
        current_promotion = None

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_collections': collections,
        'current_collection': current_collection,
        'moods_board_collection': moods_board_collection,
        'moods_board_products': moods_board_products,
        'current_promotion': current_promotion,
        'current_sorting': current_sorting,
        'collection_og_image_url': _absolute_media_url(
            request,
            uploaded_image=(current_collection.hero_image
                            if current_collection else None),
            external_url=(current_collection.hero_image_url
                          if current_collection else None),
        ),
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'product_og_image_url': _absolute_media_url(
            request,
            uploaded_image=product.image,
            external_url=product.image_url,
        ),
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
