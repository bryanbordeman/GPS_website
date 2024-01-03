from django.urls import path
from . import views

from .sitemap import StaticSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import re_path

sitemaps = {
    'pages': StaticSitemap,
}

urlpatterns = [
    path("robots.txt", views.robots_txt),
    re_path(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),
    path('', views.home, name="home"),
    path('rf_shielding/', views.rf_shielding, name="rf_shielding"),
    path('rf_chambers/', views.rf_chambers, name="rf_chambers"),
    path('radiation_shielding/', views.radiation_shielding, name="radiation_shielding"),
    path('therapy_shielding/', views.therapy_shielding, name="therapy_shielding"),
    path('lead_enclosures/', views.lead_enclosures, name="lead_enclosures"),
    path('quench_vent/', views.quench_vent, name="quench_vent"),
    path('request_quote/', views.request_quote, name="request_quote"),
    path('about_us/', views.about_us, name="about_us"),
    path('careers/', views.careers, name="careers"),
    path('services_rf_testing/', views.services_rf_testing, name="services_rf_testing"),
    path('services_engineering/', views.services_engineering, name="services_engineering"),
    path('services_door/', views.services_door, name="services_door"),
    path('scif_shielding/', views.scif_shielding, name="scif_shielding"),
    path('pd_shielding/', views.pd_shielding, name="pd_shielding"),
    path('ac_shielding/', views.ac_shielding, name="ac_shielding"),
    path('quenchCalc/', views.quenchCalc, name="quenchCalc"),
    path('radDoorCalc/', views.radDoorCalc, name="radDoorCalc"),
    path('ground_alarm/', views.ground_alarm, name="ground_alarm"),
]