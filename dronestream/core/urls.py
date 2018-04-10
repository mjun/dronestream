from django.urls import path

from dronestream.core.views import MapView

urlpatterns = [
    path('', MapView.as_view(), name='home'),
]
