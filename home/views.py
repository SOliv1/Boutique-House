from django.shortcuts import render
from django.db import OperationalError, ProgrammingError

from .models import HomePageHero, HomePromotion


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
    }
    return render(request, 'home/index.html', context)
