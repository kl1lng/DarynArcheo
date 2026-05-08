# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),

    path("artifacts/", views.artifacts_list, name="artifacts_list"),
    path("artifacts/<int:pk>/", views.artifact_detail, name="artifact_detail"),

    path("researchers/", views.researchers_list, name="researchers_list"),

    path("map/", views.map_view, name="map"),

    # API для карты (артефакты)
    path("api/artifacts.geojson/", views.artifacts_geojson, name="artifacts_geojson"),

    # Места
    path("places/", views.places_list, name="places_list"),
    path("places/<slug:slug>/", views.place_detail, name="place_detail"),

    # API для карты (места)
    path("api/places.geojson/", views.places_geojson, name="places_geojson"),

    # API для маршрутов / троп
    path("api/routes/", views.routes_geojson, name="routes_geojson"),
]
