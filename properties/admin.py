from django.utils.html import format_html
from django.contrib import admin
from .models import Property, PropertyImage, Location, Amenity
from .forms import PropertyAdminForm


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return ""

    image_preview.short_description = 'Image Preview'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # form = PropertyAdminForm
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    list_display_links = ["property_id", "title"]
    list_filter = ["create_date", "update_date"]
    inlines = [PropertyImageInline]
    filter_horizontal = ["amenities", "locations"]
    search_fields = ["title", "property_id", "create_date"]


@admin.register(Amenity)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'latitude', 'longitude')
    list_display_links = ["id", 'name', 'type', 'latitude', 'longitude']
    search_fields = ["id", 'name', 'type', 'latitude', 'longitude']


@admin.register(PropertyImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'property')
    list_display_links = ['id', 'property']
    search_fields = ['id', 'property__title', 'image']

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return ""

    image_preview.short_description = 'Image Preview'
