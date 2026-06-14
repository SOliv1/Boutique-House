from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('legal/privacy/', views.privacy_policy, name='privacy_policy'),
    path(
        'legal/terms/',
        views.terms_and_conditions,
        name='terms_and_conditions',
    ),
]
