import decimal

import requests
from django.core.management.base import BaseCommand
from django.utils import dateparse

from dronestream.core.models import Strike, Country, Province, Town


def _parse_country(strike_country):
    obj, created = Country.objects.get_or_create(name=strike_country.capitalize())
    return obj


def _parse_province(country, strike_province):
    if country and strike_province and strike_province != "Unknown":
        obj, created = Province.objects.get_or_create(country=country, name=strike_province.capitalize())
        return obj
    return None


def _parse_town(province, strike_town):
    if province and strike_town and strike_town != "Unknown":
        obj, created = Town.objects.get_or_create(province=province, name=strike_town.capitalize())
        return obj
    return None


def _parse_date(strike_date):
    return dateparse.parse_datetime(strike_date).date()


def _parse_geocoord(strike_geocoord):
    if strike_geocoord:
        return decimal.Decimal(strike_geocoord)
    return None


def _parse_int(strike_number):
    if strike_number and strike_number.isdigit():
        return int(strike_number)
    return None


def _parse_int_range(strike_number_range):
    if strike_number_range:
        if "-" in strike_number_range:
            civilians_min, civilians_max = strike_number_range.split("-")
            return _parse_int(civilians_min), _parse_int(civilians_max)
        else:
            civilians_min = civilians_max = _parse_int(strike_number_range)
            return civilians_min, civilians_max
    return None, None


def _parse_names(strike_names):
    if strike_names and isinstance(strike_names, list):
        return strike_names[0]
    return None


class Command(BaseCommand):
    help = "Imports drone strike data from https://api.dronestre.am/data"

    DRONESTREAM_API_URL = "https://api.dronestre.am/data"

    def handle(self, *args, **options):
        try:
            dronestream_request = requests.get(self.DRONESTREAM_API_URL)
        except requests.exceptions.ConnectionError:
            self.stderr.write(self.style.ERROR("Unable to load Dronestream JSON data. Failed to establish connection."))
            return

        if dronestream_request.status_code != requests.codes.ok:
            self.stderr.write(
                self.style.ERROR(
                    "Dronestream API request failed with HTTP status code {0}".format(dronestream_request.status_code)))
            return

        dronestream_json = dronestream_request.json()

        if not "status" in dronestream_json:
            self.stderr.write(
                self.style.ERROR("Unexpected response from Dronestream API. Failed to retrieve 'status' attribute."))
            return

        if dronestream_json["status"] != "OK":
            self.stderr.write(
                self.style.ERROR("Dronestream API response returned status {0}.".format(dronestream_json["status"])))
            return

        for strike_json in dronestream_json["strike"]:
            self.stdout.write(
                self.style.NOTICE("Importing strike number {0} ... ".format(strike_json["number"])), ending='')

            try:
                Strike.objects.get(number=strike_json["number"])
                self.stdout.write(self.style.WARNING("SKIP"))
            except Strike.DoesNotExist:
                strike = Strike()
                strike.dronestream_id = strike_json["_id"]
                strike.number = strike_json["number"]
                strike.date = _parse_date(strike_json["date"])
                strike.narrative = strike_json["narrative"]
                strike.country = _parse_country(strike_json["country"])
                strike.province = _parse_province(strike.country, strike_json["location"])
                strike.town = _parse_town(strike.province, strike_json["town"])
                strike.deaths_min = _parse_int(strike_json["deaths_min"])
                strike.deaths_max = _parse_int(strike_json["deaths_max"])
                strike.civilians_min, strike.civilians_max = _parse_int_range(strike_json["civilians"])
                strike.injuries_min, strike.injuries_max = _parse_int_range(strike_json["injuries"])
                strike.children_min, strike.children_max = _parse_int_range(strike_json["children"])
                strike.tweet_id = _parse_int(strike_json["tweet_id"])
                strike.bureau_id = strike_json["bureau_id"]
                strike.bij_summary_short = strike_json["bij_summary_short"]
                strike.bij_link = strike_json["bij_link"]
                strike.target = strike_json["target"]
                strike.latitude = _parse_geocoord(strike_json["lat"])
                strike.longitude = _parse_geocoord(strike_json["lon"])
                strike.names = _parse_names(strike_json["names"])
                strike.save()

                self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write(self.style.SUCCESS('Import complete'))
