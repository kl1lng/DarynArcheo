from django.contrib import admin
from .models import (
    Artifact,
    Researcher,
    Site,
    Region,
    PlaceCategory,
    Place,
    TeamMember,
)


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "period", "place", "researcher")
    list_filter = ("period", "place")
    search_fields = ("title", "description")
    list_display = ("title", "model_3d")
    # Поля, которые видны в форме редактирования артефакта
    fields = (
        "title",
        "description",
        "period",
        "photo",
        "place",          # <-- только Place
        "model_3d",
        "discovered_at",
        "researcher",
    )
    # Если хочешь жёстко скрыть site из формы на всякий случай:
    # exclude = ("site",)


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "affiliation")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")
    search_fields = ("name",)
from django.contrib import admin
from .models import Country


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0
    fields = ("name", "slug", "order")
    ordering = ("order", "name")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code", "order")
    search_fields = ("name", "iso_code")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")
    inlines = [RegionInline]

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "order")
    list_filter = ("country",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("country__order", "order", "name")


@admin.register(PlaceCategory)
class PlaceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "category", "is_featured")
    list_filter = ("region", "category", "is_featured")
    search_fields = ("name", "short_description", "long_description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")


# places/admin.py
from django.contrib import admin
from .models import Route  # плюс твои другие модели


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
