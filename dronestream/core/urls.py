from django.urls import path

from dronestream.core.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
