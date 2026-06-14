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
    path('delivery/', views.delivery_information, name='delivery_information'),
    path('track-order/', views.track_order, name='track_order'),
]
