from django.conf import settings


PRIVATE_PATH_PREFIXES = (
    '/admin/',
    '/accounts/',
    '/bag/',
    '/checkout/',
    '/profile/',
    '/track-order/',
)


def seo_settings(request):
    is_private_path = request.path.startswith(PRIVATE_PATH_PREFIXES)
    can_index = settings.SEO_INDEXING_ENABLED and not is_private_path

    return {
        'robots_directive': (
            'index, follow' if can_index else 'noindex, nofollow'
        ),
        'public_site_url': settings.PUBLIC_SITE_URL,
        'seo_indexing_enabled': settings.SEO_INDEXING_ENABLED,
    }
