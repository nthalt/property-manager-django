from django.contrib import admin
from .models import Property, PropertyImage, Location, Amenity


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    inlines = [PropertyImageInline]
    filter_horizontal = ('locations', 'amenities')
    search_fields = ["title", "property_id", "create_date"]


@admin.register(Amenity)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ["id", "name"]


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'latitude', 'longitude')
    search_fields = ["id", "name", "latitude", "longitude", "type"]


# admin.site.register(Location)
# admin.site.register(Amenity)
