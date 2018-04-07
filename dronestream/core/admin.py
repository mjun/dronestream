from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Country, Province, Town, Strike


class CountryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    actions = None
    list_per_page = 50


class ProvinceAdmin(admin.ModelAdmin):
    fields = ('country', 'name')
    list_display = ('country', 'name',)
    list_filter = ('country',)
    search_fields = ('name',)
    actions = None
    list_per_page = 50


class TownAdmin(admin.ModelAdmin):
    fields = ('province', 'name')
    list_display = ('province', 'name')
    list_filter = ('province',)
    search_fields = ('name',)
    actions = None
    list_per_page = 50


class StrikeAdminForm(forms.ModelForm):
    narrative = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}))
    names = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    bij_summary_short = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))


class StrikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("General"), {
            'fields': ('dronestream_id', 'number', 'date', 'narrative', 'tweet_id')
        }),
        (_("Location"), {
            'fields': ('country', 'province', 'town', 'latitude', 'longitude')
        }),
        (_("Details"), {
            'fields': ('target', 'deaths_min', 'deaths_max', 'civilians_min', 'civilians_max', 'injuries_min',
                       'injuries_max', 'children_min', 'children_max', 'names')
        }),
        (_("Bureau of Investigative Journalism"), {
            'fields': ('bureau_id', 'bij_summary_short', 'bij_link')
        })
    )

    form = StrikeAdminForm

    list_display = ('number', 'date', 'narrative', 'country', 'province', 'town')
    search_fields = ('narrative', 'target', 'names', 'bij_summary_short')
    actions = None
    list_per_page = 50


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Strike, StrikeAdmin)
