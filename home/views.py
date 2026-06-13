from django.shortcuts import render

from .models import HomePageHero


def index(request):
    """ A view to return the index page """
    home_hero = HomePageHero.objects.filter(is_active=True).first()
    context = {
        'home_hero': home_hero,
    }
    return render(request, 'home/index.html', context)
