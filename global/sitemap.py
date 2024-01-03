from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

class StaticSitemap(Sitemap):

    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'about_us',
            'ac_shielding',
            'careers',
            'home',
            'lead_enclosures',
            'pd_shielding',
            'request_quote',
            'scif_shielding',
            'services_door',
            'services_engineering',
            'services_rf_testing',
            'therapy_shielding',
            'rf_shielding',
            'rf_chambers',
            'radiation_shielding',
            'quench_vent',
            'ground_alarm'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
            return timezone.now()