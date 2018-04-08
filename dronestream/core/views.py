from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.views.generic import ListView

from dronestream.core.models import Strike


class HomeView(ListView):
    model = Strike
    template_name = "home.html"
    context_object_name = "strikes"

    def get_queryset(self):
        max_date = self.model.objects.all().aggregate(Max('date'))['date__max']
        min_date = max_date - relativedelta(months=3)
        return Strike.objects.filter(
            date__gte=min_date, date__lte=max_date, latitude__isnull=False, longitude__isnull=False) \
            .values('number', 'date', 'narrative', 'country__name', 'province__name', 'town__name', 'latitude',
                    'longitude')
