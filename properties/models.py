from django.core.exceptions import ValidationError
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=[
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ])
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def clean(self):
        # Case 1: Existing location name with latitude and longitude empty - should be allowed once
        if Location.objects.filter(name=self.name, latitude__isnull=True, longitude__isnull=True).exists():
            if not self.latitude and not self.longitude:
                raise ValidationError('A location with this name already exists without latitude and longitude.')

        # Case 2: Existing location name with latitude and longitude provided - should be allowed if location is different
        if self.latitude and self.longitude:
            if Location.objects.filter(name=self.name, latitude=self.latitude, longitude=self.longitude).exists():
                raise ValidationError('A location with this name and coordinates already exists.')

        # Case 3: Non-existing location name with latitude and longitude empty - should be allowed once
        if not Location.objects.filter(name=self.name).exists():
            if not self.latitude and not self.longitude:
                return  # This is allowed

        # Case 4: Existing location name with latitude and longitude provided - should be allowed if location is different
        if Location.objects.filter(name=self.name).exists():
            if not Location.objects.filter(name=self.name, latitude=self.latitude, longitude=self.longitude).exists():
                return  # This is allowed

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Amenity(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
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
    property = models.ForeignKey(
        Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.property.title}"
