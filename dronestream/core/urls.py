from django.urls import path

from dronestream.core.views import MapView, SearchView

urlpatterns = [
    path('', MapView.as_view(), name='map'),
    path('search', SearchView.as_view(), name='search'),
]
