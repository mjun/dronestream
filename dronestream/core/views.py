from django.db.models import Q
from django.views.generic import ListView

from dronestream.core.forms import StrikeFilterForm
from dronestream.core.models import Strike


class MapView(ListView):
    form_class = StrikeFilterForm
    model = Strike
    template_name = "map.html"
    context_object_name = "strikes"

    form = None
    filters = {
        'date_from': None,
        'date_to': None,
        'country': None,
        'province': None,
        'town': None
    }

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            self.form = self.form_class(self.request.GET)
            if self.form.is_valid():
                self.filters.update({
                    'date_from': self.form.cleaned_data.get('date_from'),
                    'date_to': self.form.cleaned_data.get('date_to'),
                    'country': getattr(self.form.cleaned_data.get('country'), 'id', None),
                    'province': getattr(self.form.cleaned_data.get('province'), 'id', None),
                    'town': getattr(self.form.cleaned_data.get('town'), 'id', None)
                })
                self.form = self.form_class(self.filters)
        else:
            self.form = self.form_class()
            self.filters.update({
                'date_from': self.form.fields['date_from'].initial,
                'date_to': self.form.fields['date_to'].initial
            })

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        filtered_strikes = Strike.objects.filter(latitude__isnull=False, longitude__isnull=False)

        if self.filters['date_from']:
            filtered_strikes = filtered_strikes.filter(date__gte=self.filters['date_from'])
        if self.filters['date_to']:
            filtered_strikes = filtered_strikes.filter(date__lte=self.filters['date_to'])
        if self.filters['country']:
            filtered_strikes = filtered_strikes.filter(country__id=self.filters['country'])
        if self.filters['province']:
            filtered_strikes = filtered_strikes.filter(province__id=self.filters['province'])
        if self.filters['town']:
            filtered_strikes = filtered_strikes.filter(town__id=self.filters['town'])

        return filtered_strikes.values('number', 'date', 'narrative', 'country__name', 'province__name', 'town__name',
                                       'latitude', 'longitude')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form

        return context


class SearchView(ListView):
    model = Strike
    template_name = "search.html"
    context_object_name = "strikes"

    search_string = ""
    search_terms = []

    def get(self, request, *args, **kwargs):
        self.search_string = request.GET.get('q', "").strip()
        if self.search_string:
            self.search_terms = self.search_string.split()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_terms:
            q_filters = Q()
            for term in self.search_terms:
                q_filters |= Q(country__name__icontains=term) | Q(province__name__icontains=term) | Q(
                    town__name__icontains=term) | Q(narrative__icontains=term)

            return Strike.objects.filter(q_filters)
        else:
            return Strike.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_terms'] = self.search_terms
        context['search_string'] = self.search_string

        return context
