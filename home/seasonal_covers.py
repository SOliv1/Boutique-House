from dataclasses import dataclass
from datetime import date, timedelta

from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils import timezone


SEASONAL_COVER_ROOT = 'images/collections/seasonal'
FALLBACK_COVER_PATH = (
    'images/collections/garden/boutique-banner-portrait.png'
)


@dataclass(frozen=True)
class SeasonalCover:
    season: str
    label: str
    path: str
    url: str


SEASONAL_COVERS = {
    'spring': {
        'label': 'Spring Edit',
        'filename': 'boutique-bannerSpring.png',
    },
    'summer': {
        'label': 'Summer Edit',
        'filename': 'boutique-bannerSummer.png',
    },
    'autumn': {
        'label': 'Autumn Edit',
        'filename': 'boutique-bannerAutumn.png',
    },
    'winter': {
        'label': 'Winter Edit',
        'filename': 'boutique-bannerWinter.png',
    },
}


SEASON_STARTS = (
    ((3, 1), 'spring'),
    ((6, 1), 'summer'),
    ((9, 1), 'autumn'),
    ((12, 1), 'winter'),
)


def _cover_path(season):
    filename = SEASONAL_COVERS[season]['filename']
    return f'{SEASONAL_COVER_ROOT}/{filename}'


def _first_available_cover_path(season):
    path = _cover_path(season)
    if finders.find(path):
        return path
    return FALLBACK_COVER_PATH


def _season_for_date(current_date):
    upcoming_starts = []
    for (month, day), season in SEASON_STARTS:
        upcoming_starts.append((date(current_date.year, month, day), season))
        upcoming_starts.append((date(current_date.year + 1, month, day), season))

    upcoming_starts.sort(key=lambda item: item[0])

    for start_date, season in upcoming_starts:
        if start_date - timedelta(days=7) <= current_date < start_date:
            return season

    if current_date.month in (3, 4, 5):
        return 'spring'
    if current_date.month in (6, 7, 8):
        return 'summer'
    if current_date.month in (9, 10, 11):
        return 'autumn'
    return 'winter'


def get_seasonal_cover(current_date=None):
    if current_date is None:
        current_date = timezone.localdate()

    season = _season_for_date(current_date)
    path = _first_available_cover_path(season)

    return SeasonalCover(
        season=season,
        label=SEASONAL_COVERS[season]['label'],
        path=path,
        url=static(path),
    )
