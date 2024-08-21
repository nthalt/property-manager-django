from django.core.exceptions import ValidationError
from django.db import models


class Location(models.Model):
    """
    Class for Location model
    """
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=[
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ])
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def clean(self):
        # Check if a location with the same name, type, and coordinates already exists
        if Location.objects.filter(name=self.name, type=self.type, latitude=self.latitude, longitude=self.longitude).exists():
            raise ValidationError(
                'A location with this name, type, and coordinates already exists.')

        # Check if a location with the same name and type exists without latitude and longitude
        if not self.latitude and not self.longitude:
            if Location.objects.filter(name=self.name, type=self.type, latitude__isnull=True, longitude__isnull=True).exists():
                raise ValidationError(
                    'A location with this name and type already exists without latitude and longitude.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        latitude = self.latitude if self.latitude is not None else 0
        longitude = self.longitude if self.longitude is not None else 0
        return f"{self.name} ({self.type}) (latitude: {latitude}) (longitude: {longitude})"


class Amenity(models.Model):
    """
    Class for Amenity model
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    Class for Property model
    """
    property_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    locations = models.ManyToManyField(Location)
    amenities = models.ManyToManyField(Amenity)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    """
    Class for PropertyImage model
    """
    property = models.ForeignKey(
        Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.property.title}"
