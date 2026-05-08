from django.db import models
from django.urls import reverse


class Researcher(models.Model):
    full_name = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Site(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

import os
import uuid
from django.db import models
from django.utils.text import slugify


def artifact_3d_upload_path(instance, filename):
    """
    Сохраняет 3D модель так:
    media/models3d/<slug-title>/<slug-title>-<uuid>.glb
    """
    base, ext = os.path.splitext(filename)
    ext = ext.lower()

    title_slug = slugify(instance.title) or "artifact"
    safe_name = f"{title_slug}-{uuid.uuid4().hex[:8]}{ext}"
    return f"models3d/{title_slug}/{safe_name}"

class Artifact(models.Model):
    PERIOD_CHOICES = [
        ("stone_age", "Каменный век"),
        ("bronze_age", "Бронзовый век"),
        ("iron_age", "Железный век"),
        ("medieval", "Средневековье"),
        ("modern", "Новая история"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, blank=True)
    photo = models.ImageField(upload_to='artifacts/', blank=True, null=True)
    model_3d = models.FileField(
        upload_to=artifact_3d_upload_path,
        blank=True,
        null=True,
        help_text="3D model (.glb / .gltf)"
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        related_name='artifacts',
    )

    place = models.ForeignKey(
        "Place",                    # ← ВАЖНО: в кавычках
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artifacts",
        verbose_name="Place",
    )

    discovered_at = models.DateField(blank=True, null=True)
    researcher = models.ForeignKey(Researcher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('artifact_detail', args=[self.id])

# --- НОВЫЕ МОДЕЛИ ---
class Country(models.Model):
    # Kazakhstan, Kyrgyzstan, Uzbekistan, Tajikistan, Turkmenistan
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    iso_code = models.CharField(max_length=3, blank=True)  # KZ, KG, UZ, TJ, TM (не обязательно)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="regions",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class PlaceCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Place categories"

    def __str__(self):
        return self.name


class Place(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="places")
    category = models.ForeignKey(PlaceCategory, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    photo = models.ImageField(upload_to="sites/", blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    tour_url = models.URLField(
        "Tour link",
        blank=True,
        help_text="Link to virtual tour / route / external map"
    )
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("place_detail", args=[self.slug])


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

from django.db import models


class Route(models.Model):
    name = models.CharField("Название маршрута", max_length=200)
    slug = models.SlugField("Слаг", unique=True)
    description = models.TextField("Описание", blank=True)
    color = models.CharField(
        "Цвет линии",
        max_length=20,
        default="#228b57",
    )
    coordinates = models.JSONField(
        "Координаты",
        help_text="Список точек [[lon, lat], [lon, lat], ...]",
    )

    class Meta:
        verbose_name = "маршрут"
        verbose_name_plural = "маршруты"

    def __str__(self):
        return self.name
