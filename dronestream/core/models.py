from django.db import models
from django.utils.translation import gettext as _


class Country(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=80, unique=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Province(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Name"), max_length=80, unique=True)

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


class Town(models.Model):
    province = models.ForeignKey(Province, verbose_name=_("Province"), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Name"), max_length=80)

    class Meta:
        verbose_name = _("Town")
        verbose_name_plural = _("Towns")


class Strike(models.Model):
    dronestream_id = models.CharField(verbose_name=_("Datastream ID"), max_length=80, unique=True)
    number = models.BigIntegerField(verbose_name=_("Number"), unique=True)
    date = models.DateField(verbose_name=_("Date"))
    narrative = models.CharField(verbose_name=_("Narrative"), max_length=255)
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.CASCADE)
    province = models.ForeignKey(Province, verbose_name=_("Province"), on_delete=models.CASCADE, blank=True, null=True)
    town = models.ForeignKey(Town, verbose_name=_("Town"), on_delete=models.CASCADE, blank=True, null=True)
    deaths_min = models.IntegerField(verbose_name=_("Deaths (min)"), blank=True, null=True)
    deaths_max = models.IntegerField(verbose_name=_("Deaths (max)"), blank=True, null=True)
    civilians_min = models.IntegerField(verbose_name=_("Civilians (min)"), blank=True, null=True)
    civilians_max = models.IntegerField(verbose_name=_("Civilians (max)"), blank=True, null=True)
    injuries_min = models.IntegerField(verbose_name=_("Injuries (min)"), blank=True, null=True)
    injuries_max = models.IntegerField(verbose_name=_("Injuries (max)"), blank=True, null=True)
    children_min = models.IntegerField(verbose_name=_("Children (min)"), blank=True, null=True)
    children_max = models.IntegerField(verbose_name=_("Children (max)"), blank=True, null=True)
    tweet_id = models.BigIntegerField(verbose_name="Tweet ID", blank=True, null=True)
    bureau_id = models.CharField(verbose_name=_("Bureau ID"), max_length=10, blank=True, null=True)
    bij_summary_short = models.CharField(verbose_name=_("Bureau of Investigative Journalism Summary Short"),
                                         max_length=1000, blank=True, null=True)
    bij_link = models.URLField(verbose_name=_("Bureau of Investigative Journalism Link"), blank=True, null=True)
    target = models.CharField(verbose_name=_("Target"), max_length=255, blank=True, null=True)
    latitude = models.DecimalField(verbose_name=_("Latitude"), max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(verbose_name=_("Longitude"), max_digits=10, decimal_places=8, blank=True, null=True)
    names = models.CharField(verbose_name=_("Names"), max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = _("Strike")
        verbose_name_plural = _("Strikes")
