from django.conf import settings
from django.http import HttpResponse


def robots_txt(request):
    if not settings.SEO_INDEXING_ENABLED:
        lines = [
            'User-agent: *',
            'Disallow: /',
        ]
    else:
        lines = [
            'User-agent: *',
            'Allow: /',
            'Disallow: /admin/',
            'Disallow: /accounts/',
            'Disallow: /bag/',
            'Disallow: /checkout/',
            'Disallow: /profile/',
            'Disallow: /track-order/',
            f'Sitemap: {settings.PUBLIC_SITE_URL}/sitemap.xml',
        ]

    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')
