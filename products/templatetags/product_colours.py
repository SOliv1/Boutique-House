from django import template


register = template.Library()


VINTAGE_COLOUR_SWATCHES = {
    'linen whisper': 'linen-whisper',
    'pale cream': 'pale-cream',
    'soft meadow': 'soft-meadow',
    'oyster': 'oyster',
    'peacock teal': 'peacock-teal',
    'midnight ink': 'midnight-ink',
    'ivory silk': 'ivory-silk',
    'noir shadow': 'noir-shadow',
    'rose mist': 'rose-mist',
    'blush rose': 'blush-rose',
    'rose blush': 'blush-rose',
}


@register.filter
def vintage_colourways(value):
    if not value:
        return []

    colour_names = [colour.strip() for colour in value.split(',') if colour.strip()]
    return [
        {
            'name': colour,
            'slug': VINTAGE_COLOUR_SWATCHES.get(
                colour.lower(),
                'studio-true',
            ),
        }
        for colour in colour_names
    ]
