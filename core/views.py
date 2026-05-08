from collections import defaultdict
import json

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Artifact, Researcher, Site, Region, Place, Country


# -------------------------------------------------------------------
# Главная страница + ПОИСК по артефактам и местам
# -------------------------------------------------------------------
def index(request):
    # последние артефакты для блока "Selected objects of Kazakhstan"
    latest_artifacts = (
        Artifact.objects.select_related("site")
        .order_by("-id")[:25]
    )

    # строка поиска с главной
    q = (request.GET.get("q") or "").strip()

    search_artifacts = Artifact.objects.none()
    search_places = Place.objects.none()

    if q:
        # поиск по артефактам
        search_artifacts = (
            Artifact.objects.select_related("site")
            .filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(site__name__icontains=q)
            )
        )

        # поиск по местам
        search_places = (
            Place.objects.select_related("region", "category")
            .filter(
                Q(name__icontains=q) |
                Q(short_description__icontains=q) |
                Q(long_description__icontains=q) |
                Q(region__name__icontains=q) |
                Q(category__name__icontains=q)
            )
        )

    context = {
        "latest_artifacts": latest_artifacts,
        "query": q,
        "search_artifacts": search_artifacts,
        "search_places": search_places,
    }
    return render(request, "index.html", context)


# -------------------------------------------------------------------
# Статика / простые страницы
# -------------------------------------------------------------------
def about(request):
    return render(request, "about.html")


# -------------------------------------------------------------------
# Список артефактов + фильтр по периоду + поиск
# -------------------------------------------------------------------
def artifacts_list(request):
    qs = (
        Artifact.objects.select_related("site", "researcher")
        .all()
        .order_by("-id")
    )

    period = request.GET.get("period")
    if period:
        qs = qs.filter(period=period)

    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(site__name__icontains=q) |
            Q(researcher__full_name__icontains=q)
        )

    return render(
        request,
        "artifacts_list.html",
        {"artifacts": qs, "query": q, "period": period},
    )


def artifact_detail(request, pk):
    obj = get_object_or_404(
        Artifact.objects.select_related("site", "researcher"),
        pk=pk,
    )
    return render(request, "artifact_detail.html", {"artifact": obj})


def researchers_list(request):
    return render(
        request,
        "researchers_list.html",
        {"researchers": Researcher.objects.all()},
    )


# -------------------------------------------------------------------
# Карта и GeoJSON для артефактов/мест/маршрутов
# -------------------------------------------------------------------
def map_view(request):
    return render(request, "map.html")


def artifacts_geojson(request):
    features = []

    for a in Artifact.objects.select_related("site").all():
        if not a.site:
            continue

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [a.site.longitude, a.site.latitude],
                },
                "properties": {
                    "title": a.title,
                    "period": a.get_period_display() if a.period else "",
                    "site": a.site.name,
                    "url": a.get_absolute_url(),
                },
            }
        )

    data = {"type": "FeatureCollection", "features": features}
    return JsonResponse(data)


# -------------------------------------------------------------------
# PLACES: Country -> Region -> Place + поиск
# -------------------------------------------------------------------
def places_list(request):
    q = (request.GET.get("q") or "").strip()

    countries = (
        Country.objects
        .prefetch_related(
            "regions__places",
            "regions__places__category",
        )
        .annotate(
            places_count=Count("regions__places", distinct=True)
        )
        .order_by("order", "name")
    )

    # Если нужен поиск по странице places_list — фильтруем Places внутри регионов
    # Мы сделаем это без сложных SQL: заранее найдём подходящие place_id.
    filtered_place_ids = None
    if q:
        filtered_place_ids = set(
            Place.objects.select_related("region", "category")
            .filter(
                Q(name__icontains=q) |
                Q(short_description__icontains=q) |
                Q(long_description__icontains=q) |
                Q(region__name__icontains=q) |
                Q(category__name__icontains=q)
            )
            .values_list("id", flat=True)
        )

    context = {
        "countries": countries,
        "query": q,
        "filtered_place_ids": filtered_place_ids,  # для шаблона (чтобы скрывать лишнее)
    }
    return render(request, "places_list.html", context)


def place_detail(request, slug):
    place = get_object_or_404(
        Place.objects.select_related("region", "category"),
        slug=slug,
    )
    return render(request, "place_detail.html", {"place": place})


def places_geojson(request):
    features = []
    for p in Place.objects.select_related("region", "category").all():
        if p.latitude is None or p.longitude is None:
            continue

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [p.longitude, p.latitude],  # [lon, lat]
                },
                "properties": {
                    "name": p.name,
                    "region": p.region.name if p.region else "",
                    "category": p.category.name if p.category else "",
                    "url": p.get_absolute_url(),
                },
            }
        )

    data = {"type": "FeatureCollection", "features": features}
    return JsonResponse(data)


def routes_geojson(request):
    """
    Простой пример LineString-маршрута.
    Если захочешь, можно позже заменить на более умное построение.
    """
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [67.000, 48.000],
                        [67.800, 48.200],
                        [68.300, 48.100],
                    ],
                },
                "properties": {
                    "name": "Route 1: North trail",
                    "description": "Hiking trail between Site A and Site B.",
                },
            },
        ],
    }
    return JsonResponse(data)
