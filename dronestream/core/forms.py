import datetime

from dateutil.relativedelta import relativedelta
from django import forms
from django.db.models import Max
from django.utils.translation import gettext as _

from dronestream.core.models import Country, Province, Town, Strike


class StrikeFilterForm(forms.Form):
    date_from = forms.DateField(label=_("Date from"), required=True)
    date_to = forms.DateField(label=_("Date to"), required=True)
    country = forms.ModelChoiceField(label=_("Country"), queryset=Country.objects.all().order_by('name'),
                                     required=False)
    province = forms.ModelChoiceField(label=_("Province"), queryset=Province.objects.none(), required=False)
    town = forms.ModelChoiceField(label=_("Town"), queryset=Town.objects.none(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to and date_from > date_to:
            self.add_error('date_from', _("Must be a valid date range."))
            self.add_error('date_to', _("Must be a valid date range."))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data:
            self.fields['date_to'].initial = Strike.objects.all().aggregate(Max('date'))[
                                                 'date__max'] or datetime.date.today()
            self.fields['date_from'].initial = self.fields['date_to'].initial - relativedelta(months=3)
        else:
            if 'country' in self.data and self.data['country']:
                self.fields['province'].queryset = Province.objects.filter(country__id=self.data['country']).order_by(
                    'name')
            if 'province' in self.data and self.data['province']:
                self.fields['town'].queryset = Town.objects.filter(province__id=self.data['province']).order_by('name')
